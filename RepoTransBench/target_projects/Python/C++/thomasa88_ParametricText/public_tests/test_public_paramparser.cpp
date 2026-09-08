#include <gtest/gtest.h>
#include "paramparser.h"

TEST(PublicParamParser, ParamSpecBasic) {
    auto p = ParamSpec("anotherparam", std::string("anotherval"));
    // Using .var and .member to simulate .paramName etc
    EXPECT_EQ(p.var, "anotherparam");
    ASSERT_TRUE(p.member.has_value());
    EXPECT_EQ(p.member.value(), "anotherval");
}

TEST(PublicParamParser, ParamSpecStr) {
    auto p = ParamSpec("customparam", std::string("val42"));
    std::string expected = "(customparam, val42)";
    std::ostringstream oss;
    oss << "(" << p.var;
    if (p.member) oss << ", " << p.member.value();
    oss << ")";
    EXPECT_EQ(p.to_string().substr(0, expected.size()), expected);
}

TEST(PublicParamParser, ParamSpecEq) {
    auto p1 = ParamSpec("eqtest", std::string("a"));
    auto p2 = ParamSpec("eqtest", std::string("a"));
    auto p3 = ParamSpec("eqtest", std::string("b"));
    EXPECT_TRUE(p1 == p2);
    EXPECT_FALSE(p1 == p3);
}