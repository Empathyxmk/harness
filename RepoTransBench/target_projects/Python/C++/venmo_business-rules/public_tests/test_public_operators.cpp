#include <gtest/gtest.h>
#include "business_rules/operators.h"

TEST(PublicTestStringType, contains_public) {
    StringType s("foobar");
    EXPECT_TRUE(s.contains("foo"));
    EXPECT_FALSE(s.contains("baz"));
}

// Continue for all other public operator test cases...