#include <gtest/gtest.h>
#include "parser.h"
using namespace sql_metadata;

TEST(GettingTables, SimpleQueriesTables) {
    Parser p1("SELECT * FROM `test_table`");
    EXPECT_EQ(p1.getTables(), std::vector<std::string>({"test_table"}));
    // ... Continue for rest of simple table tests, and so on for all test assertions.
}