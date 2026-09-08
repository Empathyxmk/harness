#include <gtest/gtest.h>
#include <stdexcept>
#include <string>

class PublicInit {
public:
    explicit PublicInit(std::string user = "", std::string password = "")
        : user_(user), password_(password), ready_(false)
    {
        if (!user.empty() && !password.empty()) ready_ = true;
    }
    bool isReady() const { return ready_; }
    std::string loginHint() const {
        if (user_.empty()) throw std::runtime_error("No user set");
        return "Welcome " + user_;
    }
private:
    std::string user_;
    std::string password_;
    bool ready_;
};

TEST(PublicInitTest, InitializesWhenUserAndPasswordPresent) {
    PublicInit init("demo", "pw123");
    EXPECT_TRUE(init.isReady());
}

TEST(PublicInitTest, NotReadyWhenUserOrPasswordMissing) {
    PublicInit noUser("", "pw");
    PublicInit noPw("user", "");
    EXPECT_FALSE(noUser.isReady());
    EXPECT_FALSE(noPw.isReady());
}

TEST(PublicInitTest, LoginHintWorks) {
    PublicInit init("demo", "pw123");
    EXPECT_EQ(init.loginHint(), "Welcome demo");
}

TEST(PublicInitTest, LoginHintThrowsWithNoUser) {
    PublicInit init;
    EXPECT_THROW(init.loginHint(), std::runtime_error);
}