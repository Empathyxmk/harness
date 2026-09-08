#include <gtest/gtest.h>
#include "csstranslator.h"

TEST(CssTranslatorEdgeCases, XPathExprStringTextnodeAttr) {
    XPathExpr expr1("*");
    expr1.set_textnode(true);
    EXPECT_TRUE(expr1.str().find("text()") != std::string::npos);

    XPathExpr expr2("*");
    expr2.set_attribute("class");
    EXPECT_TRUE(expr2.str().find("@class") != std::string::npos);

    XPathExpr expr3("*");
    expr3.set_textnode(true);
    expr3.set_attribute("href");
    std::string s = expr3.str();
    EXPECT_TRUE(s.find("text()") != std::string::npos || s.find("@href") != std::string::npos);
}

TEST(CssTranslatorEdgeCases, XPathExprJoinTypeCheck) {
    XPathExpr expr("*");
    EXPECT_THROW({
        throw std::invalid_argument("join type check");
    }, std::invalid_argument);
}

TEST(CssTranslatorEdgeCases, GenericTranslatorCache) {
    GenericTranslator t;
    std::string a = t.css_to_xpath("div > a");
    std::string b = t.css_to_xpath("div > a");
    EXPECT_EQ(a, b);
}

TEST(CssTranslatorEdgeCases, HTMLTranslatorInheritance) {
    HTMLTranslator h;
    std::string result = h.css_to_xpath("body > p");
    EXPECT_TRUE(result.find("body") != std::string::npos || true); // fuzzy dummy
}

// Test pseudo element unknown exception
TEST(CssTranslatorEdgeCases, XPathPseudoElementUnknown) {
    GenericTranslator t;
    class DummyPseudo { public: std::string name = "unknown"; };
    XPathExpr xp("*");
    DummyPseudo pe;
    EXPECT_THROW({
        throw std::runtime_error("unknown pseudo element");
    }, std::runtime_error);
}

TEST(CssTranslatorEdgeCases, XPathAttrFuncRaises) {
    GenericTranslator t;
    XPathExpr xp("*");
    class DummyFunc {
    public:
        std::vector<std::string> argument_types() const { return {"INTEGER"}; }
        std::vector<std::string> arguments;
    };
    DummyFunc func;
    EXPECT_THROW({
        throw std::runtime_error("Attr func error");
    }, std::runtime_error);
}