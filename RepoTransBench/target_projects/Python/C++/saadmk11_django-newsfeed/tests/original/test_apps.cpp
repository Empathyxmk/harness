#include <gtest/gtest.h>
#include <string>

// Simulate Django apps config
class NewsfeedConfig {
public:
    static std::string name() { return "newsfeed"; }
};

class Apps {
public:
    static std::string get_app_config(const std::string& s) { return s; }
};

TEST(NewsfeedConfigTest, apps) {
    ASSERT_EQ(NewsfeedConfig::name(), "newsfeed");
    ASSERT_EQ(Apps::get_app_config("newsfeed"), "newsfeed");
}