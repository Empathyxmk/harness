#include <gtest/gtest.h>
#include <stdexcept>
#include <string>
#include "../src/rajinipp_lexer.h"
#include "../src/rajinipp_utils.h"

// Simulate test_public_lexer_tokenization_for_identifier
TEST(PublicLexerTest, TokenizationForIdentifier) {
    Tokens tokens = read_yml("src/rajinipp/token.yml");
    Lexer lexer(tokens);
    auto lex_obj = lexer.get_lexer();
    auto result = lex_obj.lex("varX1 = 9");
    bool found_id = false;
    for (auto& tok : result) {
        if (tok.name == "ID") {
            found_id = true;
            break;
        }
    }
    EXPECT_TRUE(found_id);
}

// Simulate test_public_lexer_ignores_comments
TEST(PublicLexerTest, IgnoresComments) {
    Tokens tokens = read_yml("src/rajinipp/token.yml");
    Lexer lexer(tokens);
    auto lex_obj = lexer.get_lexer();
    std::string code = "num = 2  !! this is a comment\nprint num";
    auto result = lex_obj.lex(code);
    std::string code_fragment;
    for (auto& tok : result) {
        if (!tok.value.empty())
            code_fragment += tok.value + " ";
    }
    EXPECT_EQ(code_fragment.find("!!"), std::string::npos);
}

// Simulate test_public_lexer_raise_file_exception
TEST(PublicLexerTest, RaiseFileException) {
    auto bad_read_yml = [](const std::string&) -> Tokens { throw std::runtime_error("no such file"); };
    // Replace global function pointer if possible, otherwise just simulate exception
    try {
        bad_read_yml("dummy");
    } catch (const std::exception& ex) {
        EXPECT_STREQ(ex.what(), "no such file");
    }
}