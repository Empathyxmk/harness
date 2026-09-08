#include <gtest/gtest.h>
#include "pynubank/parsing.h"

TEST(ParsingTest, CanParseJson) {
    Parsing parser;
    std::string json = "{\"foo\": \"bar\"}";
    auto obj = parser.parse(json);
    EXPECT_EQ(obj["foo"], "bar");
}

TEST(ParsingTest, InvalidJsonThrows) {
    Parsing parser;
    EXPECT_THROW(parser.parse("{invalid_json}"), std::runtime_error);
}