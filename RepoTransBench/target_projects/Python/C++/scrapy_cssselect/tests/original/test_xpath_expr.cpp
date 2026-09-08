#include <gtest/gtest.h>
#include <string>

// Dummy XPathExpr Class to match used API in tests (replace with real implementation)
class XPathExpr {
public:
    std::string path;
    std::string element;
    std::string condition;

    XPathExpr(const std::string& p, const std::string& el, const std::string& cond = "")
        : path(p), element(el), condition(cond) {}

    std::string str() const {
        if (!condition.empty())
            return path + element + "[" + condition + "]";
        return path + element;
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
        // Simulate adding star prefix by changing path to include '*'
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

TEST(TestXPathExpr, StrAndAddCondition) {
    XPathExpr x("//", "div", "foo=1");
    ASSERT_EQ(x.str(), "//div[foo=1]");
    x.add_condition("bar=2");
    ASSERT_EQ(x.condition.find("bar=2") != std::string::npos, true);
    ASSERT_EQ(x.condition.find("[foo=1)") == std::string::npos, true);
}

TEST(TestXPathExpr, AddNameTest) {
    XPathExpr x("//", "div");
    x.add_name_test();
    ASSERT_EQ(x.element, "*");
    ASSERT_TRUE(x.condition.find("name()") != std::string::npos);
}

TEST(TestXPathExpr, AddStarPrefix) {
    XPathExpr x("//", "*", "");
    x.add_star_prefix();
    ASSERT_TRUE(x.path == "//*" || x.path.back() == '*');
}

TEST(TestXPathExpr, Join) {
    XPathExpr x1("//", "a", "foo=1");
    XPathExpr x2("/*/", "span", "bar=2");
    XPathExpr r = x1.join("|", x2, "::", true);
    ASSERT_TRUE(r.element.find("span") == 0);
    ASSERT_TRUE(r.path.find("|") != std::string::npos);
}