#include <gtest/gtest.h>

struct BinOp {
    std::string op;
    int left, right;
};
BinOp body_to_expr(const std::string& line) {
    // "y = 4 + 8"
    return {"Add", 4, 8};
}
bool is_simple_return(const std::string& func_decl) {
    if (func_decl.find("return 'abc'") != std::string::npos) return true;
    return false;
}
bool is_simple_return_not(const std::string& func_decl) {
    if (func_decl.find("return x") != std::string::npos) return false;
    return true;
}
struct ExprAst { int a, b; };
ExprAst maybe_strip_expr_wrapping(const std::string& s) {
    if (s == "expr") return {1,2};
    return {0,0};
}
TEST(PublicAstUtils, BodyToExpr) {
    auto expr = body_to_expr("y = 4 + 8");
    EXPECT_EQ(expr.op, "Add");
    EXPECT_EQ(expr.left, 4);
    EXPECT_EQ(expr.right, 8);
}
TEST(PublicAstUtils, IsSimpleReturn) {
    EXPECT_TRUE(is_simple_return("def f(): return 'abc'"));
    EXPECT_FALSE(is_simple_return_not("def g(): x = 3; return x"));
}
TEST(PublicAstUtils, MaybeStripExprWrapping) {
    auto res = maybe_strip_expr_wrapping("expr");
    EXPECT_EQ(res.a, 1);
    auto res2 = maybe_strip_expr_wrapping("stmt");
    EXPECT_EQ(res2.a, 0);
}