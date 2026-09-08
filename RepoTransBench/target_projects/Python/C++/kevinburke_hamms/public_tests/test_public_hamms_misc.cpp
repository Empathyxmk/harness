#include <gtest/gtest.h>
#include <algorithm>

TEST(PublicHammsMisc, Dummy) {
    ASSERT_LT(8, 10);
}

TEST(PublicHammsMisc, StringReverse) {
    std::string s = "XYZ";
    std::reverse(s.begin(), s.end());
    ASSERT_EQ(s, "ZYX");
}