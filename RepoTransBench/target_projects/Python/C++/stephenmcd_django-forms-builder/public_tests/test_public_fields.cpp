#include <gtest/gtest.h>
#include "forms_fields.h"

using namespace forms_fields;

TEST(PublicField, ToPythonBooleanTrue) {
    BooleanField boolean_field;
    EXPECT_TRUE(boolean_field.to_python("on"));
}

TEST(PublicField, ToPythonBooleanFalse) {
    BooleanField boolean_field;
    EXPECT_FALSE(boolean_field.to_python(""));
    EXPECT_FALSE(boolean_field.to_python(nullptr));
}

TEST(PublicField, ToPythonSelect) {
    SelectField select_field("orange|banana|pear");
    std::vector<std::string> expected{"orange", "banana", "pear"};
    EXPECT_EQ(select_field.choices_, expected);
}

TEST(PublicField, PrettyNameWithNumber) {
    EXPECT_EQ(pretty_name("item_123_value"), "Item 123 value");
}