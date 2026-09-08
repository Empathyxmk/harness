#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <filesystem>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <variant>
#include <memory>

#include "snap_pac/snapper_cmd.h"
#include "snap_pac/config_processor.h"

// Dummy popen simulation for snapper command call tests
class DummyPopenResult {
public:
    DummyPopenResult(const std::string &retstr) : retstr_(retstr) {}
    std::string read() { return retstr_; }
private:
    std::string retstr_;
};

using namespace snap_pac;

TEST(SnapPacSnapperCmdTest, SnapperCmdStrAndCall) {
    SnapperCmd cmd("root", "pre", "number", "desc", true, 123, "ud");
    auto s = cmd.ToString();
    EXPECT_NE(s.find("--no-dbus"), std::string::npos);
    EXPECT_NE(s.find("--config root create"), std::string::npos);
    EXPECT_NE(s.find("--description \"desc\""), std::string::npos);
    EXPECT_NE(s.find("--userdata \"ud\""), std::string::npos);
    EXPECT_NE(s.find("--type pre"), std::string::npos);

    // Simulate os.popen by lambda injection
    auto popen = [](const std::string &cmdstr) -> std::unique_ptr<DummyPopenResult> {
        return std::make_unique<DummyPopenResult>("42\n");
    };
    EXPECT_EQ(cmd.SimulateCall(popen), "42");
}

TEST(SnapPacSnapperCmdTest, SnapperCmdPostNoPrenumber) {
    SnapperCmd cmd("root", "post", "number", "", false, std::nullopt, "");
    std::string s = cmd.ToString();
    EXPECT_TRUE(s.find("--type single") != std::string::npos || s.find("--type post") != std::string::npos);

    auto popen = [](const std::string &) -> std::unique_ptr<DummyPopenResult> {
        return std::make_unique<DummyPopenResult>("test");
    };
    cmd.SimulateCall(popen);
}

TEST(SnapPacConfigProcTest, ConfigProcessorDefaultSettings) {
    std::string filename = "/tmp/cfgprocdef.ini";
    std::ofstream(filename) << "" << std::flush;
    ConfigProcessor cp(filename, "pre", "parent", {"pkg1", "pkg2"});
    auto result = cp("root");
    EXPECT_TRUE(result.description.find("parent") == 0);
    EXPECT_EQ(result.cleanup_algorithm, "number");
    std::remove(filename.c_str());
}

TEST(SnapPacConfigProcTest, ConfigProcessorIniOptions) {
    std::string filename = "/tmp/ext_ini_test.ini";
    std::ofstream ofs(filename);
    ofs << "[DEFAULT]\n";
    ofs << "snapshot = false\n";
    ofs << "cleanup_algorithm = timeline\n";
    ofs << "pre_description = mycmd\n";
    ofs << "post_description = install packages\n";
    ofs << "desc_limit = 5\n";
    ofs << "important_packages = [\"imp\"]\n";
    ofs << "important_commands = [\"imp_cmd\"]\n";
    ofs << "userdata = [\"mytag\"]\n";
    ofs << "[root]\n";
    ofs << "snapshot = true\n";
    ofs.close();

    ConfigProcessor cp(filename, "pre", "imp_cmd", {"imp", "unimp"});
    EXPECT_EQ(cp.get_cleanup_algorithm("root"), "timeline");
    EXPECT_EQ(cp.get_description("root"), "mycmd");
    EXPECT_TRUE(cp.check_important_commands("root"));
    EXPECT_TRUE(cp.check_important_packages("root"));
    std::string ud = cp.get_userdata("root");
    EXPECT_NE(ud.find("important=yes"), std::string::npos);
    EXPECT_NE(ud.find("mytag"), std::string::npos);
    auto out = cp("root");
    EXPECT_NE(out.description, "");
    EXPECT_NE(out.userdata, "");
    std::remove(filename.c_str());
}

TEST(SnapPacConfigProcTest, ConfigProcessorNonExistentSection) {
    std::string filename = "/tmp/spawnini.ini";
    std::ofstream(filename) << "" << std::flush;
    ConfigProcessor cp(filename, "post", "irrelevant", {});
    auto rv = cp("not_here");
    (void)rv.snapshot; // just check member exists
    std::remove(filename.c_str());
}

TEST(SnapPacConfigProcTest, ConfigProcessorCheckImportant) {
    std::string filename = "/tmp/imp2.ini";
    std::ofstream ofs(filename);
    ofs << "[root]\n"
           "snapshot = true\n"
           "important_packages = [\"pkgx\"]\n"
           "important_commands = [\"cmdy\"]\n"
           "userdata = [\"z\"]\n";
    ofs.close();
    ConfigProcessor cp(filename, "post", "cmdy", {"pkgx", "pkgother"});
    EXPECT_TRUE(cp.check_important("root"));
    std::remove(filename.c_str());
}

TEST(SnapPacConfigProcTest, ConfigProcessorNoImportant) {
    std::string filename = "/tmp/noimp.ini";
    std::ofstream ofs(filename);
    ofs << "[root]\n"
           "snapshot = true\n"
           "important_packages = []\n"
           "important_commands = []\n"
           "userdata = []\n";
    ofs.close();
    ConfigProcessor cp(filename, "post", "foo", {"bar"});
    EXPECT_FALSE(cp.check_important("root"));
    EXPECT_EQ(cp.get_userdata("root").find("important=yes"), std::string::npos);
    std::remove(filename.c_str());
}

TEST(SnapPacSnapperCmdTest, SnapperCmdTypes) {
    SnapperCmd cmd("abc", "post", "alg", "", false, std::nullopt, "");
    std::string s = cmd.ToString();
    EXPECT_TRUE(s.find("--type single") != std::string::npos || s.find("--type post") != std::string::npos);
}