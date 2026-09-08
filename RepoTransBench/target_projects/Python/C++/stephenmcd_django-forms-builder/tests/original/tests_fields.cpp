#include <gtest/gtest.h>
#include "forms_fields.h"

using namespace forms_fields;

TEST(Fields, LinebreakRe) {
    std::string s1 = "a\nb";
    std::string s2 = "a\r\nb";
    std::string s3 = "a\r\nb\nc";
    std::vector<std::string> want1 = {"a", "b"};
    std::vector<std::string> want2 = {"a\r", "b"};
    std::vector<std::string> want3 = {"a\r", "b", "c"};
    EXPECT_EQ(split_choices(s1), want1);
    EXPECT_EQ(split_choices(s2), want2);
    EXPECT_EQ(split_choices(s3), want3);
}

TEST(Fields, FieldTypeIterable) {
    auto types_list = FIELD_TYPES;
    EXPECT_TRUE(typeid(types_list) == typeid(std::vector<std::tuple<std::string, std::string>>));
    for (auto& t : types_list)
        EXPECT_TRUE(typeid(t) == typeid(std::tuple<std::string, std::string>) && std::tuple_size<decltype(t)>::value == 2);
}

TEST(Fields, ChoicesFromLinesBasic) {
    std::string choices = "Red\nGreen\nBlue";
    std::vector<std::string> expected = {"Red", "Green", "Blue"};
    EXPECT_EQ(choices_from_lines(choices), expected);
}

TEST(Fields, ChoicesFromLinesEmpty) {
    EXPECT_EQ(choices_from_lines(""), std::vector<std::string>());
    EXPECT_EQ(choices_from_lines(nullptr), std::vector<std::pair<std::string, std::string>>());
    EXPECT_EQ(choices_from_lines(1), std::vector<std::pair<std::string, std::string>>());
    auto out = choices_from_lines(std::vector<std::pair<std::string, std::string>>{{"foo", "foo"}});
    std::vector<std::pair<std::string, std::string>> expected = {{"foo", "foo"}};
    EXPECT_EQ(out, expected);
}