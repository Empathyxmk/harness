#include <gtest/gtest.h>
#include "parser.h"

using namespace sql_metadata;

TEST(PostgresTest, QuotedNames) {
    Parser parser1("INSERT INTO \"test\" (\"name\") VALUES ('foo') RETURNING \"test\".\"id\"");
    EXPECT_EQ(parser1.getTables(), std::vector<std::string>{"test"});
    EXPECT_EQ(parser1.getColumns(), std::vector<std::string>{"name"});
    EXPECT_EQ(parser1.getColumnsDict(), (std::map<std::string, std::vector<std::string>>{{"insert", {"name"}}}));
    EXPECT_EQ(parser1.getGeneralizedSQL(), "INSERT INTO test (name) VALUES (X) RETURNING test.id");
    EXPECT_EQ(parser1.getValues(), std::vector<std::string>{"foo"});

    Parser parser2("SELECT \"test\".\"id\", \"test\".\"name\" FROM \"test\" WHERE \"test\".\"name\" = 'foo' LIMIT 21 FOR UPDATE");
    EXPECT_EQ(parser2.getTables(), std::vector<std::string>{"test"});
    EXPECT_EQ(parser2.getColumns(), std::vector<std::string>{"test.id", "test.name"});
    EXPECT_EQ(parser2.getColumnsDict(), (std::map<std::string, std::vector<std::string>>{
        {"select", {"test.id", "test.name"}},
        {"where", {"test.name"}},
    }));
    EXPECT_EQ(parser2.getGeneralizedSQL(), "SELECT test.id, test.name FROM test WHERE test.name = X LIMIT N FOR UPDATE");

    Parser parser3("UPDATE \"test\" SET \"name\" = 'bar' WHERE \"test\".\"id\" = 1");
    EXPECT_EQ(parser3.getTables(), std::vector<std::string>{"test"});
    EXPECT_EQ(parser3.getColumns(), std::vector<std::string>{"name", "test.id"});
    EXPECT_EQ(parser3.getColumnsDict(), (std::map<std::string, std::vector<std::string>>{{"update", {"name"}, "where", {"test.id"}}}));
    EXPECT_EQ(parser3.getGeneralizedSQL(), "UPDATE test SET name = X WHERE test.id = N");
}