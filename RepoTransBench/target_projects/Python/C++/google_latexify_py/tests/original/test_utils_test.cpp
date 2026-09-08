#include <gtest/gtest.h>
#include <functional>
#include <string>
#include <vector>
#include <map>
#include <typeinfo>

// Dummy AST node/struct for demonstration
struct ASTNode {
    std::string type;
    std::map<std::string, std::string> attributes;
    std::vector<ASTNode> children;

    bool operator==(const ASTNode& other) const {
        return type == other.type && attributes == other.attributes && children == other.children;
    }
};

using TestFunction = std::function<void()>;

// Decorators: These are just helper wrappers. In C++, we simulate with versions/conditions.
bool python_minor_version = 12; // Dummy runtime value

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

// AST equality (trivial, as above)
bool ast_equal(const ASTNode& observed, const ASTNode& expected) {
    return observed == expected;
}
void assert_ast_equal(const ASTNode& observed, const ASTNode& expected) {
    ASSERT_EQ(observed, expected);
}

TEST(TestUtils, RequireAtLeastShouldCallForLowMinor) {
    bool called = false;
    auto fn = require_at_least(0, [&](){ called = true; });
    fn();
    EXPECT_TRUE(called);
}
TEST(TestUtils, RequireAtLeastShouldNotCallForHighMinor) {
    bool called = false;
    auto fn = require_at_least(python_minor_version+1, [&](){ called = true; });
    fn();
    EXPECT_FALSE(called);
}
TEST(TestUtils, RequireAtMostShouldCallForHighMinor) {
    bool called = false;
    auto fn = require_at_most(100, [&](){ called = true; });
    fn();
    EXPECT_TRUE(called);
}
TEST(TestUtils, RequireAtMostShouldNotCallForLowMinor) {
    bool called = false;
    auto fn = require_at_most(python_minor_version-1, [&](){ called = true; });
    fn();
    EXPECT_FALSE(called);
}
TEST(TestUtils, ASTEqual) {
    ASTNode a{"Add", {{"value", "3"}}, {}};
    ASTNode b{"Add", {{"value", "3"}}, {}};
    EXPECT_TRUE(ast_equal(a, b));
    assert_ast_equal(a, b);
}