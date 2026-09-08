#include <gtest/gtest.h>
#include "lexer.h"

TEST(LexerPublic, LexStringSimple) {
    std::string s = "\"xyz\"";
    auto result = pj::lexer::lex_string(s);
    EXPECT_EQ(result.first, "xyz");
    EXPECT_EQ(result.second, "");

    // no end quote (should throw)
    EXPECT_THROW(pj::lexer::lex_string("\"xyz"), std::exception);
}

TEST(LexerPublic, LexStringFail) {
    auto result = pj::lexer::lex_string("notastring");
    EXPECT_TRUE(result.first.empty());
    EXPECT_EQ(result.second, "notastring");
}

TEST(LexerPublic, LexNumberInt) {
    auto result = pj::lexer::lex_number("42 end");
    EXPECT_EQ(result.first, pj::PjValue(42));
    EXPECT_EQ(trim(result.second), "end");
    result = pj::lexer::lex_number("-11 foo");
    EXPECT_EQ(result.first, pj::PjValue(-11));
    EXPECT_EQ(trim(result.second), "foo");
}

TEST(LexerPublic, LexNumberFloat) {
    auto result = pj::lexer::lex_number("2.718rest");
    EXPECT_EQ(result.first, pj::PjValue(2.718));
    EXPECT_EQ(result.second, "rest");
    result = pj::lexer::lex_number("abc");
    EXPECT_TRUE(result.first.is_null());
    EXPECT_EQ(result.second, "abc");
}

TEST(LexerPublic, LexNumberExponent) {
    auto result = pj::lexer::lex_number("1.0e3x");
    EXPECT_EQ(result.first, pj::PjValue(1.0e3));
    EXPECT_EQ(result.second, "x");
    result = pj::lexer::lex_number("-1.2e1s");
    EXPECT_EQ(result.first, pj::PjValue(-1.2e1));
    EXPECT_EQ(result.second, "s");
}

TEST(LexerPublic, LexBoolTrueFalse) {
    auto result = pj::lexer::lex_bool("trueagain");
    EXPECT_EQ(result.first, pj::PjValue(true));
    EXPECT_EQ(result.second, "again");
    result = pj::lexer::lex_bool("falsep");
    EXPECT_EQ(result.first, pj::PjValue(false));
    EXPECT_EQ(result.second, "p");
    result = pj::lexer::lex_bool("none");
    EXPECT_TRUE(result.first.is_null());
    EXPECT_EQ(result.second, "none");
}

TEST(LexerPublic, LexNull) {
    auto result = pj::lexer::lex_null("nullness");
    EXPECT_TRUE(result.first.is_null());
    EXPECT_EQ(result.second, "ness");
    result = pj::lexer::lex_null("notnull");
    EXPECT_TRUE(result.first.is_null());
    EXPECT_EQ(result.second, "notnull");
}

TEST(LexerPublic, LexSingleWhitespace) {
    EXPECT_EQ(pj::lexer::lex(" "), std::vector<pj::PjValue>());
}

TEST(LexerPublic, LexSyntaxTokens) {
    std::vector<std::string> syntax = {",", ":", "[", "]", "{", "}"};
    for (const std::string& s : syntax) {
        EXPECT_EQ(pj::lexer::lex(s), std::vector<pj::PjValue>{pj::PjValue(s)});
    }
}

TEST(LexerPublic, LexCombined) {
    std::string s = "{\"x\": [10, \"y\", true, null]}";
    auto toks = pj::lexer::lex(s);
    std::vector<pj::PjValue> exp = {
        "{", "x", ":", "[", 10, ",", "y", ",", true, ",", pj::PjValue{}, "]", "}"
    };
    EXPECT_EQ(toks, exp);
}

TEST(LexerPublic, LexBadChar) {
    EXPECT_THROW(pj::lexer::lex("@notok"), std::exception);
}