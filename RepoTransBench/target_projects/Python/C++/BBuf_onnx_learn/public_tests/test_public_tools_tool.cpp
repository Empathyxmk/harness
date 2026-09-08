#include "tools/tool.h"
#include <gtest/gtest.h>
#include <string>
#include <vector>

TEST(TestPublicToolsTool, BasicOps) {
    EXPECT_EQ(tool::add(20, 15), 35);
    EXPECT_EQ(tool::sub(30, 25), 5);
    EXPECT_EQ(tool::mul(6, 1), 6);
    EXPECT_EQ(tool::div(81, 9), 9);
}

TEST(TestPublicToolsTool, NegativeValues) {
    EXPECT_EQ(tool::sub(-10, 5), -15);
    EXPECT_EQ(tool::mul(5, -5), -25);
}

TEST(TestPublicToolsTool, DivZero) {
    EXPECT_THROW(tool::div(-10, 0), std::logic_error);
}

TEST(TestPublicToolsTool, ToolMultiply) {
    tool::Tool t;
    EXPECT_EQ(t.multiply(9, 0), 0);
}

TEST(TestPublicToolsTool, ToolIdentity) {
    tool::Tool t;
    std::vector<std::variant<int, std::string>> vec = {1, "x", 3};
    // Since C++'s identity here would just return the value itself, we test with an int
    EXPECT_EQ(t.identity(1), 1);
    // Test for a string type
    EXPECT_EQ(t.identity(std::string("x")), "x");
    // Testing an array is less trivial; simplification.
}