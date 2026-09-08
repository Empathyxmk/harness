#include <gtest/gtest.h>
#include "jd4/case.h"

TEST(PublicCaseTest, CaseReprDiffParams)
{
    Case c("test_case2", "input-42", "output-99", 15);
    std::string r = c.to_string();
    EXPECT_NE(r.find("test_case2"), std::string::npos);
    EXPECT_NE(r.find("score=15"), std::string::npos);
}

TEST(PublicCaseTest, CasePropertiesDifferent)
{
    Case c("sampleB", "abc", "def", 8);
    EXPECT_EQ(c.name, "sampleB");
    EXPECT_EQ(c.input, "abc");
    EXPECT_EQ(c.output, "def");
    EXPECT_EQ(c.score, 8);
}

TEST(PublicCaseTest, CaseEqFalse)
{
    Case c("eqtest2", "in", "out", 1);
    EXPECT_FALSE(c == 42);
    EXPECT_TRUE(c != 42);
}

TEST(PublicCaseTest, CaseOrderingDifferentName)
{
    Case c1("case0002", "", "", 0);
    Case c2("case0010", "", "", 0);
    EXPECT_TRUE(c1 < c2);
}

TEST(PublicCaseTest, CaseStrContent)
{
    Case c("visible2", "inputY", "outputY", 4);
    std::string s = c.to_string();
    EXPECT_NE(s.find("visible2"), std::string::npos);
    EXPECT_NE(s.find("inputY"), std::string::npos);
    EXPECT_NE(s.find("outputY"), std::string::npos);
    EXPECT_NE(s.find("score=4"), std::string::npos);
}