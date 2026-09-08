#include <gtest/gtest.h>
#include <regex>
#include <string>

bool matcher(const std::string& str, const std::string& pattern) {
    std::regex re(pattern);
    return std::regex_search(str, re);
}

TEST(PublicMatcherTest, PublicSimpleMatch) {
    EXPECT_TRUE(matcher("Goal nat.", "^Goal"));
}