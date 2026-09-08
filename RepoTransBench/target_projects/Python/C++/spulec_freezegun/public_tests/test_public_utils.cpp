#include <gtest/gtest.h>
#include <cmath>

TEST(PublicUtilsTest, IsClose) {
    EXPECT_TRUE(std::fabs(13.000001 - 13.000002) < 1e-5);
}

TEST(PublicUtilsTest, Trunc) {
    EXPECT_EQ(std::trunc(152.67), 152);
}

TEST(PublicUtilsTest, Factorial) {
    int res = 1;
    for (int i = 2; i <= 6; ++i) res *= i;
    EXPECT_EQ(res, 720);
}