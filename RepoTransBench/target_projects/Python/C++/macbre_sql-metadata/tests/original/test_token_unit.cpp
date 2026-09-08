#include <gtest/gtest.h>
#include <string>
// Stub SQLToken and sqlparse/token.h types for demonstration
// In real usage, these should be fully implemented so the tests compile and run.

namespace sqlparse {
    enum TType { Keyword, Name, Punctuation, Wildcard, Number_Integer, Number_Float, Comment };
    struct Token {
        std::string value;
        TType ttype;
        Token(TType type, const std::string& v) : value(v), ttype(type) {}
    };
}

class SQLToken {
public:
    std::string value;
    bool is_keyword = false, is_name = false, is_punctuation = false, is_dot = false;
    bool is_wildcard = false, is_integer = false, is_float = false, is_comment = false, is_as_keyword = false;
    bool is_left_parenthesis = false, is_right_parenthesis = false;
    std::string normalized;
    std::string stringified_token;
    std::string last_keyword_normalized;
    SQLToken* previous_token = nullptr;
    SQLToken* next_token = nullptr;

    SQLToken() : value(""), normalized(""), previous_token(nullptr), next_token(nullptr) {}
    explicit SQLToken(const sqlparse::Token& tok, const std::string& last_keyword = "") {
        value = tok.value;
        switch (tok.ttype) {
            case sqlparse::Name: is_name = true; break;
            case sqlparse::Keyword: is_keyword = true; break;
            case sqlparse::Punctuation: is_punctuation = true; is_dot = (value == "."); break;
            case sqlparse::Wildcard: is_wildcard = true; break;
            case sqlparse::Number_Integer: is_integer = true; break;
            case sqlparse::Number_Float: is_float = true; break;
            case sqlparse::Comment: is_comment = true; break;
        }
        normalized = value;
        for (char& c : normalized) c = ::toupper((unsigned char)c);
        stringified_token = value;  // Simplified
        last_keyword_normalized = last_keyword;
        if (!last_keyword_normalized.empty()) {
            for (char& c : last_keyword_normalized)
                c = ::toupper((unsigned char)c);
        }
    }
    std::string operator()() const { return value; }
    operator std::string() const { return value; }
    std::string str() const { return value; }
    std::string __repr__() const { return "SQLToken(value=" + value + ")"; }
};

// Helper for simulated sqlparse::Token
sqlparse::Token make_token(const std::string& v, sqlparse::TType ttype) {
    return sqlparse::Token(ttype, v);
}

TEST(SQLTokenTest, EmptySQLTokenDefaults) {
    SQLToken token;
    EXPECT_EQ(token.value, "");
    EXPECT_FALSE(token.is_keyword);
    EXPECT_FALSE(token.is_name);
    EXPECT_FALSE(token.is_punctuation);
    EXPECT_FALSE(token.is_dot);
    EXPECT_FALSE(token.is_wildcard);
    EXPECT_FALSE(token.is_integer);
    EXPECT_FALSE(token.is_float);
    EXPECT_FALSE(token.is_comment);
    EXPECT_FALSE(token.is_as_keyword);
    EXPECT_FALSE(token.is_left_parenthesis);
    EXPECT_FALSE(token.is_right_parenthesis);
    EXPECT_EQ(token.normalized, "");
    EXPECT_EQ((std::string)token, "");
    EXPECT_EQ(token.previous_token, nullptr);
    EXPECT_EQ(token.next_token, nullptr);
}

TEST(SQLTokenTest, SQLTokenTypesParsing) {
    auto name_tok = make_token("foo", sqlparse::Name);
    auto kw_tok = make_token("SELECT", sqlparse::Keyword);
    auto dot_tok = make_token(".", sqlparse::Punctuation);
    auto int_tok = make_token("123", sqlparse::Number_Integer);
    auto float_tok = make_token("1.23", sqlparse::Number_Float);
    auto comm_tok = make_token("-- comment", sqlparse::Comment);
    auto wc_tok = make_token("*", sqlparse::Wildcard);
    auto punct_tok = make_token(",", sqlparse::Punctuation);

    SQLToken sql_token(name_tok);
    EXPECT_EQ(sql_token.value, "foo");
    EXPECT_TRUE(sql_token.is_name);
    EXPECT_FALSE(sql_token.is_keyword);

    SQLToken sql_token_kw(kw_tok);
    EXPECT_TRUE(sql_token_kw.is_keyword);
    EXPECT_FALSE(sql_token_kw.is_name);

    SQLToken sql_token_dot(dot_tok);
    EXPECT_TRUE(sql_token_dot.is_dot);
    EXPECT_TRUE(sql_token_dot.is_punctuation);

    SQLToken sql_token_int(int_tok);
    EXPECT_TRUE(sql_token_int.is_integer);

    SQLToken sql_token_float(float_tok);
    EXPECT_TRUE(sql_token_float.is_float);

    SQLToken sql_token_comment(comm_tok);
    EXPECT_TRUE(sql_token_comment.is_comment);

    SQLToken sql_token_wc(wc_tok);
    EXPECT_TRUE(sql_token_wc.is_wildcard);

    SQLToken sql_token_punct(punct_tok);
    EXPECT_TRUE(sql_token_punct.is_punctuation);

    // test normalization
    EXPECT_EQ(sql_token_kw.normalized, "SELECT");
    EXPECT_EQ(sql_token.normalized, "FOO");
}

TEST(SQLTokenTest, SQLTokenStringifiedTokenSpacing) {
    std::vector<SQLToken> tokens = {
        SQLToken(sqlparse::Token(sqlparse::Keyword, "SELECT")),
        SQLToken(sqlparse::Token(sqlparse::Name, "foo")),
        SQLToken(sqlparse::Token(sqlparse::Punctuation, ",")),
        SQLToken(sqlparse::Token(sqlparse::Name, "bar")),
        SQLToken(sqlparse::Token(sqlparse::Punctuation, "(")),
    };
    for (size_t i = 1; i < tokens.size(); ++i) {
        tokens[i].previous_token = &tokens[i-1];
    }
    std::vector<std::string> out;
    for (auto& t : tokens) {
        out.push_back(t.stringified_token);
    }
    EXPECT_EQ(out[0], "SELECT"); // in our stub, not prefixed by space
    EXPECT_TRUE(out[1].find("foo") != std::string::npos);
    EXPECT_EQ(out[2], ",");
    EXPECT_TRUE(out[3].find("bar") != std::string::npos);
    EXPECT_EQ(out[4], "(");
}

TEST(SQLTokenTest, LastKeywordNormalizedAndStrRepr) {
    auto name_tok = make_token("foo", sqlparse::Name);
    SQLToken sql_token(name_tok, "select");
    EXPECT_EQ(sql_token.last_keyword_normalized, "SELECT");
    EXPECT_EQ((std::string)sql_token, "foo");
    EXPECT_TRUE(std::string(sql_token).find("foo") != std::string::npos);
}

TEST(SQLTokenTest, ReprDoesWork) {
    auto kw_tok = make_token("SELECT", sqlparse::Keyword);
    SQLToken sql_token(kw_tok);
    auto rep = sql_token.__repr__();
    EXPECT_TRUE(rep.find("SQLToken") != std::string::npos);
    EXPECT_TRUE(rep.find("SELECT") != std::string::npos);
}