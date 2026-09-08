#include <gtest/gtest.h>
#include "paramparser.h"

TEST(PublicParser, ParamSpecNameValue) {
    ParamSpec spec("public_name", std::string("17"));
    EXPECT_EQ(spec.var, "public_name");
    ASSERT_TRUE(spec.member.has_value());
    EXPECT_EQ(spec.member.value(), "17");
}

TEST(PublicParser, ParamSpecStrAndEq) {
    ParamSpec spec1("ab", std::string("9"));
    ParamSpec spec2("ab", std::string("9"));
    ParamSpec spec3("ab", std::string("8"));
    std::string expected = "(ab, 9)";
    // .to_string() begins with expected
    EXPECT_EQ(spec1.to_string().substr(0, expected.size()), expected);
    EXPECT_TRUE(spec1 == spec2);
    EXPECT_FALSE(spec1 == spec3);
}