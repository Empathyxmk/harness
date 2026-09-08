#include <gtest/gtest.h>
#include <cmath>
#include <string>

TEST(PublicCode, MathOps) {
    int x = 3, y = 9;
    EXPECT_EQ(x * y, 27);
    EXPECT_DOUBLE_EQ(std::pow(y, 0.5), 3.0);
}

TEST(PublicCode, StringReverse) {
    std::string s = "abcdef";
    std::string reversed(s.rbegin(), s.rend());
    EXPECT_EQ(reversed, "fedcba");
}