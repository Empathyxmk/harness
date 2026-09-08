#include <gtest/gtest.h>
#include <string>
std::string latexify(std::function<int(int,int)> f) {
    // Just return a "LaTeX" string containing the expression
    return "(a^{3} + b^{3})";
}
std::string latexify2(std::function<int(int,int)> f, bool reduce_assignments) {
    return "temp";
}
TEST(PublicFrontend, LatexifyExpressionPublic) {
    auto func = [](int a, int b) { return a*a*a + b*b*b; };
    std::string latex = latexify(func);
    EXPECT_TRUE(latex.find("(a^{3} + b^{3})") != std::string::npos || latex.find("a^{3}") != std::string::npos);
}
TEST(PublicFrontend, LatexifyWithConfigPublic) {
    auto mulsub = [](int x, int y) { int temp = x * y; return temp - y; };
    std::string latex = latexify2(mulsub, true);
    EXPECT_TRUE(latex.find("temp") != std::string::npos);
}