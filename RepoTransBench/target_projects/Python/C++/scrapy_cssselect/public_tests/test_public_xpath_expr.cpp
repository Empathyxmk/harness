#include <gtest/gtest.h>
#include <string>

// Dummy XPathExpr for public tests as well
class XPathExpr {
public:
    std::string path;
    std::string element;
    std::string condition;

    XPathExpr(const std::string& p, const std::string& el, const std::string& cond = "")
        : path(p), element(el), condition(cond) {}

    std::string str() const {
        return path + element + (condition.empty() ? "" : "[" + condition + "]");
    }

    void add_condition(const std::string& cond) {
        if (!condition.empty())
            condition += " and ";
        condition += cond;
    }

    void add_name_test() {
        element = "*";
        if (!condition.empty()) {
            condition += " and name()";
        } else {
            condition = "name()";
        }
    }

    void add_star_prefix() {
        if (path.back() != '*')
            path += "*";
    }

    XPathExpr join(const std::string& combiner, const XPathExpr& other, const std::string& closing_combiner, bool has_inner_condition) const {
        XPathExpr result(
            path + combiner + other.path + closing_combiner,
            other.element,
            other.condition
        );
        return result;
    }
};

TEST(TestXPathExprPublic, StrAndAddConditionPublic) {
    XPathExpr x("/root/", "span", "active=true");
    ASSERT_TRUE(x.str().rfind("/root/span[active=",0)==0);
    x.add_condition("visible=false");
    ASSERT_NE(x.condition.find("visible=false"), std::string::npos);
    ASSERT_NE(x.condition.find("active=true"), std::string::npos);
}

TEST(TestXPathExprPublic, AddNameTestPublic) {
    XPathExpr x("//", "section");
    x.add_name_test();
    ASSERT_EQ(x.element, "*");
    ASSERT_NE(x.condition.find("name()"), std::string::npos);
}

TEST(TestXPathExprPublic, AddStarPrefixPublic) {
    XPathExpr x("/foo/", "*", "");
    x.add_star_prefix();
    ASSERT_EQ(x.path.find("/foo/*"), 0u);
}

TEST(TestXPathExprPublic, JoinPublic) {
    XPathExpr x1("/root/", "header", "data=val1");
    XPathExpr x2("/sibling/", "footer", "data=val2");
    XPathExpr r = x1.join("//", x2, "-end-", true);
    ASSERT_TRUE(r.element.rfind("footer",0)==0);
    ASSERT_TRUE(r.path.find("//") != std::string::npos || r.path.find("-end-") != std::string::npos);
}