#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <fstream>
#include <cstdlib>
#include <optional>
#include <memory>

#include "snap_pac/snapper_cmd.h"
#include "snap_pac/config_processor.h"

class DummyPopenResult {
public:
    DummyPopenResult(const std::string &retstr) : retstr_(retstr) {}
    std::string read() { return retstr_; }
private:
    std::string retstr_;
};

using namespace snap_pac;

TEST(PublicSnapperCmdTest, SnapperCmdStrAndCall) {
    SnapperCmd cmd("data", "pre", "timeline", "my-desc", true, 789, "user_data");
    auto s = cmd.ToString();
    EXPECT_NE(s.find("--no-dbus"), std::string::npos);
    EXPECT_NE(s.find("--config data create"), std::string::npos);
    EXPECT_NE(s.find("--description \"my-desc\""), std::string::npos);
    EXPECT_NE(s.find("--userdata \"user_data\""), std::string::npos);
    EXPECT_NE(s.find("--type pre"), std::string::npos);

    auto popen = [](const std::string &) -> std::unique_ptr<DummyPopenResult> {
        return std::make_unique<DummyPopenResult>("314\n");
    };
    EXPECT_EQ(cmd.SimulateCall(popen), "314");
}

TEST(PublicSnapperCmdTest, SnapperCmdPostNoPrenumber) {
    SnapperCmd cmd("foo", "post", "timeline", "", false, std::nullopt, "");
    std::string s = cmd.ToString();
    EXPECT_TRUE(s.find("--type single") != std::string::npos || s.find("--type post") != std::string::npos);
    auto popen = [](const std::string &) -> std::unique_ptr<DummyPopenResult> {
        return std::make_unique<DummyPopenResult>("returnz");
    };
    cmd.SimulateCall(popen);
}

TEST(PublicConfigProcTest, ConfigProcessorDefaultSettings) {
    std::string filename = "/tmp/another_config.ini";
    std::ofstream(filename) << "" << std::flush;
    ConfigProcessor cp(filename, "post", "runjob", {"abc", "xyz"});
    auto result = cp("home");
    EXPECT_TRUE(result.description.rfind("abc", 0) == 0 || result.description.rfind("runjob", 0) == 0 || result.description.rfind("xyz", 0) == 0);
    EXPECT_EQ(result.cleanup_algorithm, "number");
    std::remove(filename.c_str());
}

TEST(PublicConfigProcTest, ConfigProcessorIniOptions) {
    std::string filename = "/tmp/more_ini_test.ini";
    std::ofstream ofs(filename);
    ofs << "[DEFAULT]\n";
    ofs << "snapshot = true\n";
    ofs << "cleanup_algorithm = number\n";
    ofs << "pre_description = commandX\n";
    ofs << "post_description = just_test\n";
    ofs << "desc_limit = 6\n";
    ofs << "important_packages = [\"abc\"]\n";
    ofs << "important_commands = [\"ccc\"]\n";
    ofs << "userdata = [\"newtag\"]\n";
    ofs << "[home]\n";
    ofs << "snapshot = false\n";
    ofs.close();

    ConfigProcessor cp(filename, "pre", "ccc", {"abc", "wxy"});
    EXPECT_EQ(cp.get_cleanup_algorithm("home"), "number");
    EXPECT_EQ(cp.get_description("home"), "comman");
    EXPECT_TRUE(cp.check_important_commands("home"));
    EXPECT_TRUE(cp.check_important_packages("home"));
    std::string ud = cp.get_userdata("home");
    EXPECT_NE(ud.find("important=yes"), std::string::npos);
    EXPECT_NE(ud.find("newtag"), std::string::npos);
    auto out = cp("home");
    EXPECT_NE(out.description, "");
    EXPECT_NE(out.userdata, "");
    std::remove(filename.c_str());
}

TEST(PublicConfigProcTest, ConfigProcessorNonExistentSection) {
    std::string filename = "/tmp/section.ini";
    std::ofstream(filename) << "" << std::flush;
    ConfigProcessor cp(filename, "pre", "diff", {});
    auto rv = cp("qwerty");
    EXPECT_TRUE(rv.description.size() >= 0); // Check member exists
    std::remove(filename.c_str());
}

TEST(PublicConfigProcTest, ConfigProcessorCheckImportant) {
    std::string filename = "/tmp/zzz.ini";
    std::ofstream ofs(filename);
    ofs << "[home]\n"
           "snapshot = false\n"
           "important_packages = [\"specialpkg\"]\n"
           "important_commands = [\"specialcmd\"]\n"
           "userdata = [\"t\"]\n";
    ofs.close();
    ConfigProcessor cp(filename, "post", "specialcmd", {"specialpkg", "otherpkg"});
    EXPECT_TRUE(cp.check_important("home"));
    std::remove(filename.c_str());
}

TEST(PublicConfigProcTest, ConfigProcessorNoImportant) {
    std::string filename = "/tmp/notag.ini";
    std::ofstream ofs(filename);
    ofs << "[zzz]\n"
           "snapshot = false\n"
           "important_packages = []\n"
           "important_commands = []\n"
           "userdata = []\n";
    ofs.close();
    ConfigProcessor cp(filename, "post", "nope", {"nil"});
    EXPECT_FALSE(cp.check_important("zzz"));
    EXPECT_EQ(cp.get_userdata("zzz").find("important=yes"), std::string::npos);
    std::remove(filename.c_str());
}

TEST(PublicSnapperCmdTest, SnapperCmdTypes) {
    SnapperCmd cmd("customcfg", "post", "otheralg", "", false, std::nullopt, "");
    std::string s = cmd.ToString();
    EXPECT_TRUE(s.find("--type single") != std::string::npos || s.find("--type post") != std::string::npos);
}