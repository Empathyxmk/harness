#include <gtest/gtest.h>
#include "paramparser.h"

TEST(TestParamSpec, FromStringBasic) {
    auto ps = ParamSpec::from_string("foo");
    ASSERT_TRUE(ps.has_value());
    EXPECT_TRUE(*ps == ParamSpec("foo"));
}

TEST(TestParamSpec, FromStringWithMember) {
    auto ps = ParamSpec::from_string("foo.bar");
    ASSERT_TRUE(ps.has_value());
    EXPECT_TRUE(*ps == ParamSpec("foo", std::string("bar")));
}

TEST(TestParamSpec, FromStringWithSlice) {
    auto ps = ParamSpec::from_string("foo[2]");
    ASSERT_TRUE(ps.has_value());
    EXPECT_TRUE(*ps == ParamSpec("foo", std::nullopt, std::make_pair(2,3)));
    auto ps2 = ParamSpec::from_string("foo[1:3]");
    ASSERT_TRUE(ps2.has_value());
    EXPECT_TRUE(*ps2 == ParamSpec("foo", std::nullopt, std::make_pair(1,3)));
    auto ps3 = ParamSpec::from_string("foo[:4]");
    ASSERT_TRUE(ps3.has_value());
    EXPECT_TRUE(*ps3 == ParamSpec("foo", std::nullopt, std::make_pair(-99999,4)));
    auto ps4 = ParamSpec::from_string("foo[-2:]");
    ASSERT_TRUE(ps4.has_value());
    EXPECT_TRUE(*ps4 == ParamSpec("foo", std::nullopt, std::make_pair(-2,99999)));
}

TEST(TestParamSpec, FromStringWithFormat) {
    auto ps = ParamSpec::from_string("foo:0.2f");
    ASSERT_TRUE(ps.has_value());
    EXPECT_TRUE(*ps == ParamSpec("foo", std::nullopt, std::nullopt, std::string("0.2f")));
    ps = ParamSpec::from_string("foo.bar[0:2]:spec");
    ASSERT_TRUE(ps.has_value());
    EXPECT_TRUE(*ps == ParamSpec("foo", std::string("bar"), std::make_pair(0,2), std::string("spec")));
}

TEST(TestParamSpec, FromStringInvalid) {
    auto ps = ParamSpec::from_string("bad[");
    EXPECT_FALSE(ps.has_value());
}

TEST(TestParamSpec, EqOp) {
    ParamSpec a("foo", std::string("bar"), std::make_pair(1,2), std::string("fmt"));
    ParamSpec b("foo", std::string("bar"), std::make_pair(1,2), std::string("fmt"));
    ParamSpec c("foo", std::string("baz"), std::make_pair(1,2), std::string("fmt"));
    EXPECT_TRUE(a == b);
    EXPECT_FALSE(a == c);
    EXPECT_FALSE(a == ParamSpec("foo", std::nullopt, std::make_pair(1,2), std::string("fmt"))); // member differs
}

TEST(TestParamSpec, Nullint) {
    EXPECT_EQ(nullint("3"), 3);
    EXPECT_EQ(nullint(""), -1);
}