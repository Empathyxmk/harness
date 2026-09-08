#include <gtest/gtest.h>
#include "parser.h"

TEST(ParserPublic, ParseArrayEmpty) {
    auto [val, tokens] = pj::parser::parse_array({"]"});
    EXPECT_EQ(val, pj::PjValue::array({}));
    EXPECT_TRUE(tokens.empty());
}

TEST(ParserPublic, ParseArrayMultiple) {
    std::vector<pj::PjValue> toks = {100, ",", 200, "]", "remain"};
    auto [arr, rest] = pj::parser::parse_array(toks);
    EXPECT_EQ(arr, pj::PjValue::array({pj::PjValue(100), pj::PjValue(200)}));
    EXPECT_EQ(rest, std::vector<pj::PjValue>{"remain"});
}

TEST(ParserPublic, ParseArrayError) {
    EXPECT_THROW(pj::parser::parse_array({100, 200, "]"}), std::exception);
}

TEST(ParserPublic, ParseObjectEmpty) {
    auto [val, tokens] = pj::parser::parse_object({"}"});
    EXPECT_EQ(val, pj::PjValue::object({}));
    EXPECT_TRUE(tokens.empty());
}

TEST(ParserPublic, ParseObjectBasic) {
    std::vector<pj::PjValue> toks = {"x", ":", 1, "}"};
    auto [obj, rest] = pj::parser::parse_object(toks);
    EXPECT_EQ(obj, pj::PjValue::object({{"x", pj::PjValue(1)}}));
    EXPECT_TRUE(rest.empty());
}

TEST(ParserPublic, ParseObjectMultiple) {
    std::vector<pj::PjValue> toks = {"foo", ":", 7, ",", "bar", ":", 8, "}", "left"};
    auto [obj, rest] = pj::parser::parse_object(toks);
    EXPECT_EQ(obj, pj::PjValue::object({{"foo", pj::PjValue(7)}, {"bar", pj::PjValue(8)}}));
    EXPECT_EQ(rest, std::vector<pj::PjValue>{"left"});
}

TEST(ParserPublic, ParseObjectKeyNonstring) {
    EXPECT_THROW(pj::parser::parse_object({100, ":", 2, "}"}), std::exception);
}

TEST(ParserPublic, ParseObjectColonMissing) {
    EXPECT_THROW(pj::parser::parse_object({"x", 2, "}"}), std::exception);
}

TEST(ParserPublic, ParseObjectCommaMissing) {
    EXPECT_THROW(pj::parser::parse_object({"x", ":", 2, 5, "}"}), std::exception);
}

TEST(ParserPublic, ParseArrayMissingEnd) {
    EXPECT_THROW(pj::parser::parse_array({1, ","}), std::exception);
}

TEST(ParserPublic, ParseObjectMissingEnd) {
    EXPECT_THROW(pj::parser::parse_object({"z", ":", 3}), std::exception);
}

TEST(ParserPublic, ParseRootNonObject) {
    EXPECT_THROW(pj::parser::parse({"[", 2, "]"}, true), std::exception);
}

TEST(ParserPublic, ParseArrayDelegation) {
    auto [arr, rest] = pj::parser::parse({"[", 10, ",", 11, "]"});
    EXPECT_EQ(arr, pj::PjValue::array({pj::PjValue(10), pj::PjValue(11)}));
    EXPECT_TRUE(rest.empty());
}

TEST(ParserPublic, ParseObjectDelegation) {
    auto [obj, rest] = pj::parser::parse({"{", "foo", ":", 12, "}"});
    EXPECT_EQ(obj, pj::PjValue::object({{"foo", pj::PjValue(12)}}));
    EXPECT_TRUE(rest.empty());
}

TEST(ParserPublic, ParseLiteral) {
    auto [val, rest] = pj::parser::parse({2, ",", 99});
    EXPECT_EQ(val, pj::PjValue(2));
    EXPECT_EQ(rest, std::vector<pj::PjValue>{",", 99});
}