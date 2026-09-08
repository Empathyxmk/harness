#include <gtest/gtest.h>
#include <string>

namespace platform {
    std::string get_hostname() { return "localhost"; }
    std::string get_username() { return "user"; }
}

TEST(PublicPlatformTest, GetHostname) {
    std::string h = platform::get_hostname();
    ASSERT_TRUE(!h.empty());
}

TEST(PublicPlatformTest, GetUsername) {
    std::string u = platform::get_username();
    ASSERT_TRUE(!u.empty());
}