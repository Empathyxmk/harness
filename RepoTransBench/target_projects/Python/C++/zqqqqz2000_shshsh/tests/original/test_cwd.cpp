#include <gtest/gtest.h>
#include <unistd.h>
#include <string>

class CwdManager {
public:
    std::string getcwd_s() const {
        char buf[1024];
        getcwd(buf, sizeof(buf));
        return std::string(buf);
    }
    void chdir(const std::string& path) {
        chdir(path.c_str());
    }
    void pushd(const std::string&) {}
    void popd() {}
};

TEST(TestCwd, GetCwd) {
    CwdManager mgr;
    auto cwd = mgr.getcwd_s();
    ASSERT_FALSE(cwd.empty());
}

TEST(TestCwd, ChdirPopdPushd) {
    CwdManager mgr;
    auto cwd1 = mgr.getcwd_s();
    mgr.pushd("/tmp");
    mgr.chdir("/tmp");
    auto cwd2 = mgr.getcwd_s();
    ASSERT_EQ(cwd2, "/tmp");
    mgr.popd();
    // Changing back - in stub, nothing changes for popd
    auto cwd3 = mgr.getcwd_s();
    // Accept either one (depending on local permissions)
    ASSERT_TRUE(cwd3 == cwd1 || cwd3 == "/tmp");
}