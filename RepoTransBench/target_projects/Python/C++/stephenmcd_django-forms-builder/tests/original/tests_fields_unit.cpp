#include <gtest/gtest.h>
#include "forms_fields.h"

using namespace forms_fields;

TEST(FieldsUnit, SplitChoicesString) {
    std::string s = "Red\nBlue\r\nGreen";
    std::vector<std::string> result = split_choices(s);
    std::vector<std::string> expected = {"Red", "Blue\r", "Green"};
    EXPECT_EQ(result, expected);
}

TEST(FieldsUnit, SplitChoicesEmpty) {
    EXPECT_EQ(split_choices(""), std::vector<std::string>());
    EXPECT_EQ(split_choices(nullptr), std::vector<std::pair<std::string, std::string>>());
    EXPECT_EQ(split_choices(0), std::vector<std::pair<std::string, std::string>>());
    EXPECT_EQ(split_choices(3.14), std::vector<std::pair<std::string, std::string>>());
}

TEST(FieldsUnit, SplitChoicesListOfTuples) {
    std::vector<std::pair<std::string, std::string>> lst = {{"A", "Apple"}, {"B", "Banana"}};
    EXPECT_EQ(split_choices(lst), lst);
}

TEST(FieldsUnit, SplitChoicesTupleOfTuples) {
    // C++ doesn't distinguish between tuple/list of tuples and tuple of tuples for logic above
    std::vector<std::pair<std::string, std::string>> tpl = {{"A", "Apple"}, {"B", "Banana"}};
    EXPECT_EQ(split_choices(tpl), tpl);
}

TEST(FieldsUnit, SplitChoicesLeadingTrailingWhitespace) {
    std::string s = " Red \n\n Blue";
    std::vector<std::string> result = split_choices(s);
    std::vector<std::string> expected = {" Red ", " Blue"};
    EXPECT_EQ(result, expected);
}

TEST(FieldsUnit, AliasChoicesFromLines) {
    std::string s = "One\nTwo";
    std::vector<std::string> result = choices_from_lines(s);
    std::vector<std::string> expected = {"One", "Two"};
    EXPECT_EQ(result, expected);
}

TEST(FieldsUnit, FieldChoicesAndTypes) {
    EXPECT_TRUE(typeid(FIELD_CHOICES) == typeid(std::vector<std::tuple<std::string, std::string>>));
    EXPECT_TRUE(typeid(FIELD_TYPES) == typeid(std::vector<std::tuple<std::string, std::string>>));
    for (auto& i : FIELD_TYPES)
        EXPECT_TRUE(typeid(i) == typeid(std::tuple<std::string, std::string>));
    EXPECT_EQ(FIELD_TYPES, FIELD_CHOICES);
}