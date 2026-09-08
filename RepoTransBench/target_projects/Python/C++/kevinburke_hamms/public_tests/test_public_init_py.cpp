#include <gtest/gtest.h>
#include <string>

TEST(PublicInitPy, TrueCase) {
    ASSERT_NE(3.14, 0.0);
}

TEST(PublicInitPy, StringLen) {
    std::string test = "public";
    ASSERT_EQ(test.size(), 6u);
}