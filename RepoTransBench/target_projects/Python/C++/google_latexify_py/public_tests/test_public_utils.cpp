#include <gtest/gtest.h>
#include <functional>
#include <string>
#include <vector>
#include <map>

// Simulate a decorator mechanism in C++ with lambdas as earlier
bool python_minor_version = 12;

using TestFunction = std::function<void()>;

TestFunction require_at_least(int minor, TestFunction fn) {
    return [minor, fn]() {
        if (python_minor_version < minor) return;
        fn();
    };
}
TestFunction require_at_most(int minor, TestFunction fn) {
    return [minor, fn]() {
        if (python_minor_version > minor) return;
        fn();
    };
}

// Dummy AST node as in test_utils_test.cpp
struct ASTNode {
    std::string type;
    std::map<std::string, std::string> attributes;
    std::vector<ASTNode> children;
    bool operator==(const ASTNode& other) const {
        return type == other.type && attributes == other.attributes && children == other.children;
    }
};

bool ast_equal(const ASTNode& observed, const ASTNode& expected) {
    return observed == expected;
}
void assert_ast_equal(const ASTNode& observed, const ASTNode& expected) {
    ASSERT_EQ(observed, expected);
}

TEST(PublicUtils, RequireAtLeastDecorator) {
    bool called = false;
    auto f = require_at_least(0, [&](){ called = true; });
    f();
    EXPECT_TRUE(called);

    called = false;
    auto f2 = require_at_least(python_minor_version+1, [&](){ called = true; });
    f2();
    EXPECT_FALSE(called);
}
TEST(PublicUtils, RequireAtMostDecorator) {
    bool called = false;
    auto f = require_at_most(100, [&](){ called = true; });
    f();
    EXPECT_TRUE(called);

    called = false;
    auto f2 = require_at_most(python_minor_version-1, [&](){ called = true; });
    f2();
    EXPECT_FALSE(called);
}
TEST(PublicUtils, AstEqualAndAssertAstEqualSimple) {
    ASTNode observed{"Assign", {{"target","b"},{"value","3"}}, {}};
    ASTNode expected{"Assign", {{"target","b"},{"value","3"}}, {}};
    EXPECT_TRUE(ast_equal(observed, expected));
    assert_ast_equal(observed, expected);
}
TEST(PublicUtils, AstEqualAndAssertAstEqualExpr) {
    ASTNode observed{"Add", {{"left","x"},{"right","2"}}, {}};
    ASTNode expected{"Add", {{"left","x"},{"right","2"}}, {}};
    EXPECT_TRUE(ast_equal(observed, expected));
    assert_ast_equal(observed, expected);
}