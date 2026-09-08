#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <filesystem>
#include <cstdio>
#include <cstdlib>
#include <fstream>

#include "snap_pac/snapper_cmd.h"
#include "snap_pac/config_processor.h"
#include "snap_pac/get_snapper_configs.h"
#include "snap_pac/check_skip.h"
#include "snap_pac/prefile.h"

// Fixture for parametric snapper command string representations
struct SnapperCmdStrTestCase {
    snap_pac::SnapperCmd cmd;
    std::string expected_cmd;
};

class SnapperCmdStrTest : public ::testing::TestWithParam<SnapperCmdStrTestCase> {};

INSTANTIATE_TEST_SUITE_P(
    SnapperCmdStrTests,
    SnapperCmdStrTest,
    ::testing::Values(
        SnapperCmdStrTestCase{
            snap_pac::SnapperCmd("root", "pre", "number", "foo"),
            "snapper --config root create --cleanup-algorithm number --print-number --description \"foo\" --type pre"
        },
        SnapperCmdStrTestCase{
            snap_pac::SnapperCmd("root", "post", "number", "bar", false, 1234),
            "snapper --config root create --cleanup-algorithm number --print-number --description \"bar\" --pre-number 1234 --type post"
        },
        SnapperCmdStrTestCase{
            snap_pac::SnapperCmd("root", "post", "number", "bar", true, 1234),
            "snapper --no-dbus --config root create --cleanup-algorithm number --print-number --description \"bar\" --pre-number 1234 --type post"
        },
        SnapperCmdStrTestCase{
            snap_pac::SnapperCmd("root", "post", "number", "bar", false, 1234, "important=yes"),
            "snapper --config root create --cleanup-algorithm number --print-number --description \"bar\" --userdata \"important=yes\" --pre-number 1234 --type post"
        },
        SnapperCmdStrTestCase{
            snap_pac::SnapperCmd("root", "post", "number", "bar", false, 1234, "foo=bar,important=yes"),
            "snapper --config root create --cleanup-algorithm number --print-number --description \"bar\" --userdata \"foo=bar,important=yes\" --pre-number 1234 --type post"
        },
        SnapperCmdStrTestCase{
            snap_pac::SnapperCmd("root", "post", "number", "bar", false, std::nullopt, "foo=bar,important=yes"),
            "snapper --config root create --cleanup-algorithm number --print-number --description \"bar\" --userdata \"foo=bar,important=yes\" --type single"
        }
    )
);

TEST_P(SnapperCmdStrTest, ToString) {
    auto param = GetParam();
    EXPECT_EQ(param.cmd.ToString(), param.expected_cmd);
}

TEST(SnapPacScriptTest, GetSnapperConfigs) {
    // create a temporary file
    std::string filename;
    {
        char tmpname[] = "/tmp/snapperconfigXXXXXX";
        int fd = mkstemp(tmpname);
        ASSERT_NE(fd, -1);
        std::ofstream ofs(tmpname);
        ofs << "## Path: System/Snapper\n\n";
        ofs << "## Type:        string\n";
        ofs << "## Default:     \"\"\n";
        ofs << "# List of snapper configurations.\n";
        ofs << "SNAPPER_CONFIGS=\"home root foo bar\"\n";
        ofs.close();
        filename = tmpname;
        close(fd);
    }
    auto configs = snap_pac::get_snapper_configs(filename);
    std::vector<std::string> expected{"home", "root", "foo", "bar"};
    EXPECT_EQ(configs, expected);
    std::remove(filename.c_str());
}

TEST(SnapPacScriptTest, SkipSnapPac) {
    setenv("SNAP_PAC_SKIP", "y", 1);
    EXPECT_TRUE(snap_pac::check_skip());
    unsetenv("SNAP_PAC_SKIP");
}

struct ConfigProcessorTestCase {
    std::string section;
    std::string command;
    std::vector<std::string> packages;
    std::string snapshot_type;
    snap_pac::ConfigProcessorExpected result;
};

class ConfigProcessorTest : public ::testing::TestWithParam<ConfigProcessorTestCase> {};

INSTANTIATE_TEST_SUITE_P(
    ConfigProcessorTests,
    ConfigProcessorTest,
    ::testing::Values(
        ConfigProcessorTestCase{
            "root", "foo", {"bar"}, "pre",
            {"foo", "number", "", true}
        },
        ConfigProcessorTestCase{
            "root", "pacman -Syu", {}, "pre",
            {"pacman -Syu", "number", "important=yes", true}
        },
        ConfigProcessorTestCase{
            "mail", "pacman -Syu", {}, "pre",
            {"pacman -Syu", "number", "", false}
        },
        ConfigProcessorTestCase{
            "home", "pacman -Syu", {}, "pre",
            {"pac", "number", "foo=bar,requestid=42", true}
        },
        ConfigProcessorTestCase{
            "home", "pacman -Syu", {}, "post",
            {"a r", "number", "foo=bar,requestid=42", true}
        },
        ConfigProcessorTestCase{
            "myconfig", "pacman -S linux", {"linux"}, "post",
            {"linux", "timeline", "foo=bar,important=yes,requestid=42", true}
        }
    )
);

TEST_P(ConfigProcessorTest, ConfigProcessorBehaves) {
    auto param = GetParam();
    // Create temp ini file for config
    std::string filename;
    {
        char tmpname[] = "/tmp/cfgprocessXXXXXX";
        int fd = mkstemp(tmpname);
        ASSERT_NE(fd, -1);
        std::ofstream ofs(tmpname);
        ofs << "[root]\n";
        ofs << "important_commands = [\"pacman -Syu\"]\n\n";
        ofs << "[home]\n";
        ofs << "snapshot = True\n";
        ofs << "desc_limit = 3\n";
        ofs << "post_description = a really long description\n";
        ofs << "userdata = [\"foo=bar\", \"requestid=42\"]\n\n";
        ofs << "[myconfig]\n";
        ofs << "snapshot = True\n";
        ofs << "cleanup_algorithm = timeline\n";
        ofs << "important_packages = [\"linux\", \"linux-lts\"]\n";
        ofs << "userdata = [\"foo=bar\", \"requestid=42\"]\n";
        ofs.close();
        filename = tmpname;
        close(fd);
    }
    snap_pac::ConfigProcessor config_processor(filename, param.snapshot_type, param.command, param.packages);
    auto out = config_processor(param.section);
    EXPECT_EQ(out, param.result);
    std::remove(filename.c_str());
}

TEST(SnapPacScriptTest, PrefileReadNone) {
    snap_pac::Prefile prefile("root", "pre");
    EXPECT_EQ(prefile.read(), std::nullopt);
}

TEST(SnapPacScriptTest, PrefileReadWrite) {
    snap_pac::Prefile prefile("root", "pre");
    prefile.write("1234");
    snap_pac::Prefile prefile_post("root", "post");
    EXPECT_EQ(prefile_post.read(), std::optional<std::string>("1234"));
    // cleanup
    prefile.cleanup();
    prefile_post.cleanup();
}

TEST(SnapPacScriptTest, NoPrefile) {
    snap_pac::Prefile prefile("foo-pre-file-not-found", "post");
    EXPECT_EQ(prefile.read(), std::nullopt);
}