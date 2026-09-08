#include <gtest/gtest.h>
#include "lexer.h"

TEST(Lexer, LexStringSimple) {
    std::string s = "\"abc\"";
    auto result = pj::lexer::lex_string(s);
    EXPECT_EQ(result.first, "abc");
    EXPECT_EQ(result.second, "");

    // no end quote (should throw)
    EXPECT_THROW(pj::lexer::lex_string("\"abc"), std::exception);
}

TEST(Lexer, LexStringFail) {
    auto result = pj::lexer::lex_string("notstring");
    EXPECT_TRUE(result.first.empty()); // Equivalent of None in C++
    EXPECT_EQ(result.second, "notstring");
}

TEST(Lexer, LexNumberInt) {
    auto result = pj::lexer::lex_number("123 end");
    EXPECT_EQ(result.first, pj::PjValue(123));
    EXPECT_EQ(trim(result.second), "end");
    result = pj::lexer::lex_number("-55 foo");
    EXPECT_EQ(result.first, pj::PjValue(-55));
    EXPECT_EQ(trim(result.second), "foo");
}

TEST(Lexer, LexNumberFloat) {
    auto result = pj::lexer::lex_number("3.14rest");
    EXPECT_EQ(result.first, pj::PjValue(3.14));
    EXPECT_EQ(result.second, "rest");
    // no number at start
    result = pj::lexer::lex_number("abc");
    EXPECT_TRUE(result.first.is_null());
    EXPECT_EQ(result.second, "abc");
}

TEST(Lexer, LexNumberValidExponent) {
    auto result = pj::lexer::lex_number("1.23e2foo");
    EXPECT_EQ(result.first, pj::PjValue(1.23e2));
    EXPECT_EQ(result.second, "foo");
    result = pj::lexer::lex_number("-3.2e2z");
    EXPECT_EQ(result.first, pj::PjValue(-3.2e2));
    EXPECT_EQ(result.second, "z");
}

TEST(Lexer, LexBoolTrueFalse) {
    auto result = pj::lexer::lex_bool("trueabc");
    EXPECT_EQ(result.first, pj::PjValue(true));
    EXPECT_EQ(result.second, "abc");
    result = pj::lexer::lex_bool("falsex");
    EXPECT_EQ(result.first, pj::PjValue(false));
    EXPECT_EQ(result.second, "x");
    // Not bool
    result = pj::lexer::lex_bool("null");
    EXPECT_TRUE(result.first.is_null());
    EXPECT_EQ(result.second, "null");
}

TEST(Lexer, LexNull) {
    auto result = pj::lexer::lex_null("nullvalue");
    EXPECT_TRUE(result.first.is_null());
    EXPECT_EQ(result.second, "value");
    // Not null
    result = pj::lexer::lex_null("none");
    EXPECT_TRUE(result.first.is_null());
    EXPECT_EQ(result.second, "none");
}

TEST(Lexer, LexSingleWhitespace) {
    EXPECT_EQ(pj::lexer::lex(" "), std::vector<pj::PjValue>());
}

TEST(Lexer, LexSyntaxTokens) {
    std::vector<std::string> syntax = {",", ":", "[", "]", "{", "}"};
    for (const std::string& s : syntax) {
        EXPECT_EQ(pj::lexer::lex(s), std::vector<pj::PjValue>{pj::PjValue(s)});
    }
}

TEST(Lexer, LexCombined) {
    std::string s = "{\"foo\": [123, \"bar\", false, null]}";
    auto toks = pj::lexer::lex(s);
    // Build expected vector
    std::vector<pj::PjValue> exp = {
        "{", "foo", ":", "[", 123, ",", "bar", ",", false, ",", pj::PjValue{}, "]", "}"
    };
    EXPECT_EQ(toks, exp);
}

TEST(Lexer, LexBadChar) {
    EXPECT_THROW(pj::lexer::lex("$notvalid"), std::exception);
}