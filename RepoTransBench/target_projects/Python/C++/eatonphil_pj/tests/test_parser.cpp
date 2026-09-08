#include <gtest/gtest.h>
#include "parser.h"

TEST(Parser, ParseArrayEmpty) {
    auto [val, tokens] = pj::parser::parse_array({"]"});
    EXPECT_EQ(val, pj::PjValue::array({}));
    EXPECT_TRUE(tokens.empty());
}

TEST(Parser, ParseArrayMultiple) {
    std::vector<pj::PjValue> toks = {1, ",", 2, "]", "leftover"};
    auto [arr, rest] = pj::parser::parse_array(toks);
    EXPECT_EQ(arr, pj::PjValue::array({pj::PjValue(1), pj::PjValue(2)}));
    EXPECT_EQ(rest, std::vector<pj::PjValue>{"leftover"});
}

TEST(Parser, ParseArrayError) {
    EXPECT_THROW(pj::parser::parse_array({1, 2, "]"}), std::exception);
}

TEST(Parser, ParseObjectEmpty) {
    auto [val, tokens] = pj::parser::parse_object({"}"});
    EXPECT_EQ(val, pj::PjValue::object({}));
    EXPECT_TRUE(tokens.empty());
}

TEST(Parser, ParseObjectBasic) {
    std::vector<pj::PjValue> toks = {"key", ":", 42, "}"};
    auto [obj, rest] = pj::parser::parse_object(toks);
    EXPECT_EQ(obj, pj::PjValue::object({{"key", pj::PjValue(42)}}));
    EXPECT_TRUE(rest.empty());
}

TEST(Parser, ParseObjectMultiple) {
    std::vector<pj::PjValue> toks = {"a", ":", 1, ",", "b", ":", 2, "}", "end"};
    auto [obj, rest] = pj::parser::parse_object(toks);
    EXPECT_EQ(obj, pj::PjValue::object({{"a", pj::PjValue(1)}, {"b", pj::PjValue(2)}}));
    EXPECT_EQ(rest, std::vector<pj::PjValue>{"end"});
}

TEST(Parser, ParseObjectKeyNonstring) {
    EXPECT_THROW(pj::parser::parse_object({1, ":", 2, "}"}), std::exception);
}

TEST(Parser, ParseObjectColonMissing) {
    EXPECT_THROW(pj::parser::parse_object({"key", 42, "}"}), std::exception);
}

TEST(Parser, ParseObjectCommaMissing) {
    EXPECT_THROW(pj::parser::parse_object({"key", ":", 1, 42, "}"}), std::exception);
}

TEST(Parser, ParseArrayMissingEnd) {
    EXPECT_THROW(pj::parser::parse_array({1, ","}), std::exception);
}

TEST(Parser, ParseObjectMissingEnd) {
    EXPECT_THROW(pj::parser::parse_object({"key", ":", 1}), std::exception);
}

TEST(Parser, ParseRootNonObject) {
    EXPECT_THROW(pj::parser::parse({"[", 1, "]"}, true), std::exception);
}

TEST(Parser, ParseArrayDelegation) {
    auto [arr, rest] = pj::parser::parse({"[", 1, ",", 2, "]"});
    EXPECT_EQ(arr, pj::PjValue::array({pj::PjValue(1), pj::PjValue(2)}));
    EXPECT_TRUE(rest.empty());
}

TEST(Parser, ParseObjectDelegation) {
    auto [obj, rest] = pj::parser::parse({"{", "a", ":", 3, "}"});
    EXPECT_EQ(obj, pj::PjValue::object({{"a", pj::PjValue(3)}}));
    EXPECT_TRUE(rest.empty());
}

TEST(Parser, ParseLiteral) {
    auto [val, rest] = pj::parser::parse({42, ",", 100});
    EXPECT_EQ(val, pj::PjValue(42));
    EXPECT_EQ(rest, std::vector<pj::PjValue>{",", 100});
}