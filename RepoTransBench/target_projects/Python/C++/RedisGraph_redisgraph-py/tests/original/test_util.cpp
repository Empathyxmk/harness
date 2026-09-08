#include <gtest/gtest.h>
#include "util.h"
#include <string>
#include <vector>
#include <map>
#include <variant>
#include <algorithm>
#include <type_traits>

using namespace redisgraph;

// Helper to check if a variant index corresponds to string or int, etc.
// Assume Value in util.h is a std::variant<std::string, int, double, bool, std::nullptr_t,
// std::vector<Value>, std::map<std::string, Value>>, as is typical for these APIs.

TEST(TestUtil, RandomStringLength) {
    std::vector<size_t> tests = {1, 5, 10, 32};
    for (size_t n : tests) {
        std::string s = random_string(n);
        EXPECT_EQ(s.length(), n);
    }
}

TEST(TestUtil, QuoteStringBasic) {
    EXPECT_EQ(quote_string("abc"), "\"abc\"");
    EXPECT_EQ(quote_string(std::string("bytes")), "\"bytes\"");
    EXPECT_EQ(quote_string(""), "\"\"");
    EXPECT_EQ(quote_string("he\"llo"), "\"he\\\"llo\"");
    EXPECT_EQ(quote_string("back\\slash"), "\"back\\\\slash\"");
    // If we pass an int, returns string of int
    EXPECT_EQ(quote_string(123), "123");
}

TEST(TestUtil, StringifyParamValueBasic) {
    EXPECT_EQ(stringify_param_value("foo"), "\"foo\"");
    EXPECT_EQ(stringify_param_value(nullptr), "null");

    // List with int, None, string
    std::vector<Value> v1 = {Value(1), Value(nullptr), Value(std::string("x"))};
    EXPECT_EQ(stringify_param_value(v1), "[1,null,\"x\"]");

    // Tuple-like (use vector for sequence)
    std::vector<Value> v2 = {Value(2), Value(3)};
    EXPECT_EQ(stringify_param_value(v2), "[2,3]");

    // Dict/unordered: can be {a:1,b:"z"} or {b:"z",a:1}
    std::map<std::string, Value> m = {{"a", Value(1)}, {"b", Value(std::string("z"))}};
    auto s = stringify_param_value(m);
    bool dict_ok = (s == "{a:1,b:\"z\"}" || s == "{b:\"z\",a:1}");
    EXPECT_TRUE(dict_ok);

    EXPECT_EQ(stringify_param_value(3.14), "3.14");
    EXPECT_EQ(stringify_param_value(7), "7");
}