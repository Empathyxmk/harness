#include <gtest/gtest.h>
#include "../../src/rajinipp_lexer.h"
#include "../../src/rajinipp_exceptions.h"

TEST(LexerTest, AddAndGetTokens) {
    Tokens tokens({{"NUM", "\\d+"}, {"PLUS", "\\+"}});
    Lexer lexer(tokens);
    auto lex_obj = lexer.get_lexer();
    EXPECT_TRUE(lex_obj.has_lex_method());
    auto result = lex_obj.lex("3 + 5");
    std::set<std::string> names;
    for (auto &tok : result) names.insert(tok.name);
    EXPECT_EQ(names, std::set<std::string>({"NUM", "PLUS"}));
}

TEST(LexerTest, IgnoreCommentsAndWhitespace) {
    Tokens tokens({{"ID", "[a-zA-Z_]+"}, {"EQ", "="}});
    Lexer lexer(tokens);
    auto lex_obj = lexer.get_lexer();
    std::string code = "foo = bar   !! this is a comment\nbaz=qux";
    auto result = lex_obj.lex(code);
    std::vector<std::string> names;
    for (auto &tok : result) names.push_back(tok.name);
    std::vector<std::string> expect = {"ID", "EQ", "ID", "ID", "EQ", "ID"};
    EXPECT_EQ(names, expect);
}

TEST(ExceptionsTest, BreakException) {
    EXPECT_THROW(throw BreakException("Break now"), BreakException);
}

TEST(ExceptionsTest, ReturnExceptionValue) {
    try {
        throw ReturnException("Return!", 42);
    } catch (const ReturnException& e) {
        EXPECT_EQ(e.return_value, 42);
        EXPECT_NE(std::string(e.what()).find("Return!"), std::string::npos);
    }
}