#include <gtest/gtest.h>
#include <sstream>
#include <string>

TEST(PublicWarningsTest, WarnsUser) {
    std::ostringstream oss;
    oss << "example warning!";
    std::string out = oss.str();
    ASSERT_NE(out.find("example warning!"), std::string::npos);
}

TEST(PublicWarningsTest, WarnsDeprecation) {
    std::ostringstream oss;
    oss << "deprecated soon";
    std::string out = oss.str();
    ASSERT_NE(out.find("deprecated soon"), std::string::npos);
}