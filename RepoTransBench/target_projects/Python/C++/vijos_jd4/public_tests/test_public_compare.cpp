#include <gtest/gtest.h>
#include "jd4/compare.h"

TEST(PublicCompareTest, StripTrailingSpacesNewlines)
{
    std::string s = "hello world    \n  \n\t";
    EXPECT_EQ(strip_trailing_spaces_newlines(s), "hello world");
}

TEST(PublicCompareTest, ComparePublicEqualNorm)
{
    std::string a = "foo bar   \n";
    std::string b = "foo bar";
    bool eq = compare_stream(a, b);
    EXPECT_TRUE(eq);
}

TEST(PublicCompareTest, ComparePublicNotEqual)
{
    std::string a = "value1";
    std::string b = "value2";
    bool eq = compare_stream(a, b);
    EXPECT_FALSE(eq);
}