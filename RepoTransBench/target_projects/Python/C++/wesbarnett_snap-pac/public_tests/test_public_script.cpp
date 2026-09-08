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

struct PubSnapperCmdTestCase {
    snap_pac::SnapperCmd cmd;
    std::string expected_cmd;
};

class PublicSnapperCmdStrTest : public ::testing::TestWithParam<PubSnapperCmdTestCase> {};

INSTANTIATE_TEST_SUITE_P(
    PublicSnapperCmdStrTests,
    PublicSnapperCmdStrTest,
    ::testing::Values(
        PubSnapperCmdTestCase{
            snap_pac::SnapperCmd("data", "pre", "timeline", "baz"),
            "snapper --config data create --cleanup-algorithm timeline --print-number --description \"baz\" --type pre"
        },
        PubSnapperCmdTestCase{
            snap_pac::SnapperCmd("home", "post", "timeline", "qux", false, 4321),
            "snapper --config home create --cleanup-algorithm timeline --print-number --description \"qux\" --pre-number 4321 --type post"
        },
        PubSnapperCmdTestCase{
            snap_pac::SnapperCmd("data", "post", "timeline", "quux", true, 5678),
            "snapper --no-dbus --config data create --cleanup-algorithm timeline --print-number --description \"quux\" --pre-number 5678 --type post"
        },
        PubSnapperCmdTestCase{
            snap_pac::SnapperCmd("foo", "post", "timeline", "snap", false, 8765, "bar=foo"),
            "snapper --config foo create --cleanup-algorithm timeline --print-number --description \"snap\" --userdata \"bar=foo\" --pre-number 8765 --type post"
        },
        PubSnapperCmdTestCase{
            snap_pac::SnapperCmd("home", "post", "timeline", "test", false, 2468, "alpha=beta,gamma=delta"),
            "snapper --config home create --cleanup-algorithm timeline --print-number --description \"test\" --userdata \"alpha=beta,gamma=delta\" --pre-number 2468 --type post"
        },
        PubSnapperCmdTestCase{
            snap_pac::SnapperCmd("data", "post", "timeline", "snap", false, std::nullopt, "foo=bar,baz=qux"),
            "snapper --config data create --cleanup-algorithm timeline --print-number --description \"snap\" --userdata \"foo=bar,baz=qux\" --type single"
        }
    )
);

TEST_P(PublicSnapperCmdStrTest, StrCmp) {
    auto param = GetParam();
    EXPECT_EQ(param.cmd.ToString(), param.expected_cmd);
}

TEST(PublicScriptTest, GetSnapperConfigs) {
    std::string filename;
    {
        char tmpname[] = "/tmp/snappubconfigXXXXXX";
        int fd = mkstemp(tmpname);
        ASSERT_NE(fd, -1);
        std::ofstream ofs(tmpname);
        ofs << "## Path: System/Snapper\n\n";
        ofs << "## Type:        string\n";
        ofs << "## Default:     \"\"\n";
        ofs << "# List of snapper configurations.\n";
        ofs << "SNAPPER_CONFIGS=\"data home alpha beta\"\n";
        ofs.close();
        filename = tmpname;
        close(fd);
    }
    auto configs = snap_pac::get_snapper_configs(filename);
    std::vector<std::string> expected{"data", "home", "alpha", "beta"};
    EXPECT_EQ(configs, expected);
    std::remove(filename.c_str());
}

TEST(PublicScriptTest, SkipSnapPac) {
    setenv("SNAP_PAC_SKIP", "yes", 1);
    EXPECT_TRUE(snap_pac::check_skip());
    unsetenv("SNAP_PAC_SKIP");
}

struct PublicConfigProcessorTestCase {
    std::string section;
    std::string command;
    std::vector<std::string> packages;
    std::string snapshot_type;
    snap_pac::ConfigProcessorExpected result;
};

class PublicConfigProcessorTest : public ::testing::TestWithParam<PublicConfigProcessorTestCase> {};

INSTANTIATE_TEST_SUITE_P(
    PublicConfigProcessorTests,
    PublicConfigProcessorTest,
    ::testing::Values(
        PublicConfigProcessorTestCase{
            "home", "bar", {"qux"}, "pre",
            {"bar", "timeline", "", true}
        },
        PublicConfigProcessorTestCase{
            "data", "apt-get update", {}, "pre",
            {"apt-get update", "timeline", "critical=yes", true}
        },
        PublicConfigProcessorTestCase{
            "archive", "apt-get update", {}, "pre",
            {"apt-get update", "timeline", "", false}
        },
        PublicConfigProcessorTestCase{
            "beta", "apt-get update", {}, "pre",
            {"apt", "timeline", "foo=bar,requestid=99", true}
        },
        PublicConfigProcessorTestCase{
            "beta", "apt-get update", {}, "post",
            {"test d", "timeline", "foo=bar,requestid=99", true}
        },
        PublicConfigProcessorTestCase{
            "special", "apt-get install kernel", {"kernel"}, "post",
            {"kernel", "number", "foo=bar,critical=yes,requestid=99", true}
        }
    )
);

TEST_P(PublicConfigProcessorTest, PublicConfigProcBehaves) {
    auto param = GetParam();
    std::string filename;
    {
        char tmpname[] = "/tmp/pubcfgprocessXXXXXX";
        int fd = mkstemp(tmpname);
        ASSERT_NE(fd, -1);
        std::ofstream ofs(tmpname);
        ofs << "[home]\n";
        ofs << "important_commands = [\"apt-get update\"]\n\n";
        ofs << "cleanup_algorithm = timeline\n";
        ofs << "[beta]\n";
        ofs << "snapshot = True\n";
        ofs << "desc_limit = 5\n";
        ofs << "post_description = test description for beta section\n";
        ofs << "userdata = [\"foo=bar\", \"requestid=99\"]\n\n";
        ofs << "[special]\n";
        ofs << "snapshot = True\n";
        ofs << "cleanup_algorithm = number\n";
        ofs << "important_packages = [\"kernel\", \"initrd\"]\n";
        ofs << "userdata = [\"foo=bar\", \"requestid=99\"]\n";
        ofs.close();
        filename = tmpname;
        close(fd);
    }
    snap_pac::ConfigProcessor cp(filename, param.snapshot_type, param.command, param.packages);
    auto out = cp(param.section);
    EXPECT_EQ(out, param.result);
    std::remove(filename.c_str());
}

TEST(PublicPrefileTest, PrefileReadNone) {
    snap_pac::Prefile prefile("data", "pre");
    EXPECT_EQ(prefile.read(), std::nullopt);
}

TEST(PublicPrefileTest, PrefileReadWrite) {
    snap_pac::Prefile prefile("home", "pre");
    prefile.write("5678");
    snap_pac::Prefile prefile_post("home", "post");
    EXPECT_EQ(prefile_post.read(), std::optional<std::string>("5678"));
    prefile.cleanup();
    prefile_post.cleanup();
}

TEST(PublicPrefileTest, NoPrefile) {
    snap_pac::Prefile prefile("nonexistent-pre-file", "post");
    EXPECT_EQ(prefile.read(), std::nullopt);
}