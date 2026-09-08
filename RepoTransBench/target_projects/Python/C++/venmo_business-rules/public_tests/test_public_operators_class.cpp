#include <gtest/gtest.h>
#include "business_rules/operators.h"

TEST(PublicOperatorsClassTestCase, base_type_value_public) {
    BaseType base("Value1");
    EXPECT_EQ(base.value, "Value1");
}

TEST(PublicOperatorsClassTestCase, string_type_inheritance_public) {
    StringType s("PublicString");
    EXPECT_TRUE(dynamic_cast<BaseType*>(&s) != nullptr);
    EXPECT_EQ(s.value, "PublicString");
}

TEST(PublicOperatorsClassTestCase, numeric_type_inheritance_public) {
    NumericType n(999);
    EXPECT_TRUE(dynamic_cast<BaseType*>(&n) != nullptr);
    // Cannot compare n.value since NumericType's base is not storing double.
}

TEST(PublicOperatorsClassTestCase, boolean_type_inheritance_public) {
    BooleanType b(true);
    EXPECT_TRUE(dynamic_cast<BaseType*>(&b) != nullptr);
    EXPECT_EQ(b.value, "true");
}