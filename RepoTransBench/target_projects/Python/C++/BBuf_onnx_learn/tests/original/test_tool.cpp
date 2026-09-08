#include "tools/tool.h"
#include <gtest/gtest.h>
#include <string>

TEST(TestToolFunctions, Add) {
    EXPECT_EQ(tool::add(1, 2), 3);
    EXPECT_EQ(tool::add(-2, 2), 0);
    EXPECT_EQ(tool::add(0, 0), 0);
}

TEST(TestToolFunctions, Sub) {
    EXPECT_EQ(tool::sub(3, 2), 1);
    EXPECT_EQ(tool::sub(-1, 1), -2);
}

TEST(TestToolFunctions, Mul) {
    EXPECT_EQ(tool::mul(3, 2), 6);
    EXPECT_EQ(tool::mul(0, 8), 0);
}

TEST(TestToolFunctions, Div) {
    EXPECT_EQ(tool::div(6, 3), 2);
    EXPECT_THROW(tool::div(3, 0), std::logic_error);
}

TEST(TestToolFunctions, ToolClass) {
    tool::Tool t;
    EXPECT_EQ(t.multiply(2, 3), 6);
    EXPECT_EQ(t.identity(10), 10);
    // Verify identity function is callable: compile-time check
    EXPECT_TRUE((std::is_same<decltype(t.identity(10)), int>::value));
}