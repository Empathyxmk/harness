#include "tools/tool.h"
#include <gtest/gtest.h>
#include <string>

TEST(TestToolsTool, BasicOps) {
    EXPECT_EQ(tool::add(10, 5), 15);
    EXPECT_EQ(tool::sub(10, 5), 5);
    EXPECT_EQ(tool::mul(4, 0), 0);
    EXPECT_EQ(tool::div(20, 4), 5);
}

TEST(TestToolsTool, NegativeValues) {
    EXPECT_EQ(tool::sub(-5, -5), 0);
    EXPECT_EQ(tool::mul(-2, 3), -6);
}

TEST(TestToolsTool, DivZero) {
    EXPECT_THROW(tool::div(1, 0), std::logic_error);
}

TEST(TestToolsTool, ToolMultiply) {
    tool::Tool t;
    EXPECT_EQ(t.multiply(-1, 8), -8);
}

TEST(TestToolsTool, ToolIdentity) {
    tool::Tool t;
    EXPECT_EQ(t.identity(std::string("abc")), "abc");
}