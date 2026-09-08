#include <gtest/gtest.h>
#include <string>
// #include "utils.h"

std::string alphanumeric_only(const std::string& input) {
    std::string result;
    for (char c : input) {
        if (isalnum(c)) result += c;
    }
    return result;
}

TEST(PublicUtilsTest, AlphanumericOnlyPublic) {
    EXPECT_EQ(alphanumeric_only("xyz789GH@#!"), "xyz789GH");
    EXPECT_EQ(alphanumeric_only(" **&$  321 "), "321");
}