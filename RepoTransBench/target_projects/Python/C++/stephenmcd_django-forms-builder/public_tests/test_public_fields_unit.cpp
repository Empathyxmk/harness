#include <gtest/gtest.h>
#include "forms_fields.h"

using namespace forms_fields;

TEST(PublicFieldsUnit, PublicSplitChoicesDiffInput) {
    std::string value = "red|green|blue";
    std::vector<std::string> choices = split_choices(value, "|");
    std::vector<std::string> expected = {"red", "green", "blue"};
    EXPECT_EQ(choices, expected);
}

TEST(PublicFieldsUnit, PublicPrettyNameDiffInput) {
    std::string val = "zip_code";
    EXPECT_EQ(pretty_name(val), "Zip code");
}

TEST(PublicFieldsUnit, PublicIsEmptyDiffInput) {
    EXPECT_TRUE(is_empty(nullptr));
    std::vector<std::string> not_empty = {"value"};
    EXPECT_FALSE(is_empty(not_empty));
    EXPECT_TRUE(is_empty("      "));
}