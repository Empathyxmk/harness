#include <gtest/gtest.h>
#include "business_rules/operators.h"
#include <string>
#include <vector>
#include <cmath>
#include <stdexcept>

TEST(StringOperatorTests, operator_decorator) {
    StringType st("foo");
    EXPECT_TRUE(st.equal_to.is_operator);
}

TEST(StringOperatorTests, string_equal_to) {
    StringType a("foo");
    EXPECT_TRUE(a.equal_to("foo"));
    EXPECT_FALSE(a.equal_to("Foo"));
}

TEST(StringOperatorTests, string_equal_to_case_insensitive) {
    StringType a("foo");
    EXPECT_TRUE(a.equal_to_case_insensitive("FOo"));
    EXPECT_TRUE(a.equal_to_case_insensitive("foo"));
    EXPECT_FALSE(a.equal_to_case_insensitive("blah"));
}

// and so on for every Python unittest in the file