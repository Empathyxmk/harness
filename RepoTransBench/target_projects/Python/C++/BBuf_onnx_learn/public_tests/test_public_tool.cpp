#include "tools/tool.h"
#include <gtest/gtest.h>
#include <string>

TEST(TestPublicToolFunctions, Add) {
    EXPECT_EQ(tool::add(5, 7), 12);
    EXPECT_EQ(tool::add(-3, 3), 0);
    EXPECT_EQ(tool::add(10, -10), 0);
}

TEST(TestPublicToolFunctions, Sub) {
    EXPECT_EQ(tool::sub(10, 2), 8);
    EXPECT_EQ(tool::sub(-10, 5), -15);
}

TEST(TestPublicToolFunctions, Mul) {
    EXPECT_EQ(tool::mul(7, 3), 21);
    EXPECT_EQ(tool::mul(-4, 2), -8);
}

TEST(TestPublicToolFunctions, Div) {
    EXPECT_EQ(tool::div(8, 2), 4);
    EXPECT_THROW(tool::div(-4, 0), std::logic_error);
}

TEST(TestPublicToolFunctions, ToolClass) {
    tool::Tool t;
    EXPECT_EQ(t.multiply(4, -2), -8);
    EXPECT_EQ(t.identity(0), 0);
    EXPECT_TRUE((std::is_same<decltype(t.identity(0)), int>::value));
}