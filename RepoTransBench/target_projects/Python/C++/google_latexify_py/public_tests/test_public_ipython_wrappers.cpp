#include <gtest/gtest.h>
#include <string>
struct DummyFunc {
    std::string latex;
    DummyFunc(const std::string& lx) : latex(lx) {}
    std::string _latex_() { return latex; }
};
std::string _repr_latex_(DummyFunc& d) { return d._latex_(); }

template<typename Dummy>
void register_latex_for_functions(Dummy&) { /* Just ensures set */ }

TEST(PublicIPythonWrappers, ReprLatexPublic) {
    DummyFunc dummy("A_{test}");
    std::string result = _repr_latex_(dummy);
    EXPECT_EQ(result, "A_{test}");
}
TEST(PublicIPythonWrappers, RegisterLatexForFunctionsPublic) {
    struct Dummy { int marker=0; static std::string _latex_() { return "L"; } };
    Dummy d;
    register_latex_for_functions(d);
    EXPECT_EQ(Dummy::_latex_(), "L");
}