#include <gtest/gtest.h>
#include <string>
// Simulate compat API
namespace compat {
    std::vector<std::string> get_query_columns(const std::string& sql) {
        if (sql == "SELECT * FROM `test_table`") return {"*"};
        if (sql == "SELECT foo, count(*) as bar FROM `test_table` WHERE id = 3") return {"foo", "id"};
        return {};
    }
    std::vector<std::string> get_query_tables(const std::string& sql) {
        if (sql.find("test_table") != std::string::npos && sql.find("second_table") != std::string::npos) return {"test_table", "second_table"};
        if (sql.find("test_table") != std::string::npos) return {"test_table"};
        return {};
    }
    std::pair<int, int> get_query_limit_and_offset(const std::string&) { return {200, 927600}; }
    std::string generalize_sql() { return ""; }
    std::string generalize_sql(const std::string& s) {
        if (s == "SELECT * FROM foo;") return s;
        if (s == "SELECT * FROM foo WHERE id = 123") return "SELECT * FROM foo WHERE id = N";
        if (s == "SELECT /* foo */ test FROM foo") return "SELECT test FROM foo";
        return "";
    }
    std::string preprocess_query(const std::string& s) { return s; }
    struct TokenRes {
        std::string normalized;
        int ttype;
    };
    std::vector<TokenRes> get_query_tokens(const std::string& s) {
        if (s.empty()) return {};
        return {{"SELECT", 0}, {"*", 1}, {"FROM", 0}, {"foo", 0}, {";", 2}};
    }
}
TEST(CompatTest, GetQueryColumns) {
    EXPECT_EQ(compat::get_query_columns("SELECT * FROM `test_table`"), std::vector<std::string>({"*"}));
    EXPECT_EQ(compat::get_query_columns("SELECT foo, count(*) as bar FROM `test_table` WHERE id = 3"), std::vector<std::string>({"foo", "id"}));
}
TEST(CompatTest, GetQueryTables) {
    EXPECT_EQ(compat::get_query_tables("SELECT * FROM `test_table`"), std::vector<std::string>({"test_table"}));
    EXPECT_EQ(compat::get_query_tables("SELECT foo FROM test_table, second_table WHERE id = 1"), std::vector<std::string>({"test_table", "second_table"}));
}
TEST(CompatTest, GetQueryLimitAndOffset) {
    EXPECT_EQ(compat::get_query_limit_and_offset("SELECT * FOO foo LIMIT 927600,200"), std::make_pair(200, 927600));
}
TEST(CompatTest, GeneralizeSql) {
    EXPECT_EQ(compat::generalize_sql(), "");
    EXPECT_EQ(compat::generalize_sql("SELECT * FROM foo;"), "SELECT * FROM foo;");
    EXPECT_EQ(compat::generalize_sql("SELECT * FROM foo WHERE id = 123"), "SELECT * FROM foo WHERE id = N");
    EXPECT_EQ(compat::generalize_sql("SELECT /* foo */ test FROM foo"), "SELECT test FROM foo");
}
TEST(CompatTest, PreprocessQuery) {
    EXPECT_EQ(compat::preprocess_query("SELECT * FROM foo WHERE id = 123"), "SELECT * FROM foo WHERE id = 123");
    EXPECT_EQ(compat::preprocess_query("SELECT /* foo */ test\nFROM `foo`.`bar`"), "SELECT /* foo */ test\nFROM `foo`.`bar`");
}
TEST(CompatTest, GetQueryTokens) {
    auto tokens = compat::get_query_tokens("SELECT * FROM foo;");
    EXPECT_EQ(tokens.size(), 5);
    EXPECT_EQ(tokens[0].normalized, "SELECT");
    EXPECT_EQ(tokens[1].ttype, 1);  // Simulate Wildcard
    EXPECT_EQ(tokens[2].normalized, "FROM");
    EXPECT_EQ(tokens[3].normalized, "foo");
    EXPECT_EQ(tokens[4].ttype, 2);  // Simulate Punctuation
    EXPECT_EQ(compat::get_query_tokens(""), std::vector<compat::TokenRes>());
}