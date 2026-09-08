#include <gtest/gtest.h>
#include "parser.h"
#include "keywords_lists.h"
using namespace sql_metadata;

TEST(TruncateTable, Truncate) {
    Parser parser("TRUNCATE TABLE foo");
    EXPECT_EQ(parser.getQueryType(), QueryType::TRUNCATE);
    EXPECT_EQ(parser.getTables(), std::vector<std::string>{"foo"});
    EXPECT_EQ(parser.getColumns(), std::vector<std::string>{});
}