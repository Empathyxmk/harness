#include <gtest/gtest.h>
#include "parser.h"

using namespace sql_metadata;

TEST(ColumnAliases, ColumnAliasesWithSubquery) {
    std::string query = R"SQL(
    SELECT yearweek(SignDate) as                         Aggregation,
       BusinessSource,
       (SELECT sum(C2Count)
        from (SELECT count(C2) as C2Count, BusinessSource,
        yearweek(Start1) Start1, yearweek(End1) End1
              from (
                       SELECT ContractID as C2, BusinessSource, StartDate as Start1,
                       EndDate as End1
                       from data_contracts_report
                   ) sq2
              group by 2, 3, 4) sq
        where Start1 <= yearweek(SignDate)
          and End1 >= yearweek(SignDate)
          and sq.BusinessSource = mq.BusinessSource) CountOfConsultants
FROM data_contracts_report mq
where SignDate >= last_day(date_add(now(), interval -13 month))
group by 1, 2
order by 1, 2;
    )SQL";
    Parser parser(query);
    EXPECT_EQ(parser.getTables(), std::vector<std::string>{"data_contracts_report"});
    EXPECT_EQ(parser.getSubqueryNames(), std::vector<std::string>{"sq2", "sq"});
    std::map<std::string, std::string> expected_subqueries = {
        {"sq", "SELECT count(C2) as C2Count, BusinessSource, yearweek(Start1) Start1, yearweek(End1) End1 from (SELECT ContractID as C2, BusinessSource, StartDate as Start1, EndDate as End1 from data_contracts_report) sq2 group by 2, 3, 4"},
        {"sq2", "SELECT ContractID as C2, BusinessSource, StartDate as Start1, EndDate as End1 from data_contracts_report"}
    };
    EXPECT_EQ(parser.getSubqueries(), expected_subqueries);
    EXPECT_EQ(parser.getColumns(), (std::vector<std::string>{"SignDate", "BusinessSource", "ContractID", "StartDate", "EndDate", "data_contracts_report.BusinessSource"}));
    EXPECT_EQ(parser.getColumnAliasesNames(), (std::vector<std::string>{"Aggregation", "C2Count", "Start1", "End1", "C2", "CountOfConsultants"}));
    auto aliases = parser.getColumnAliases();
    EXPECT_TRUE(std::get<std::string>(aliases["Aggregation"]) == "SignDate");
    EXPECT_TRUE(std::get<std::string>(aliases["C2"]) == "ContractID");
    EXPECT_TRUE(std::get<std::string>(aliases["C2Count"]) == "C2");
    EXPECT_TRUE(std::get<std::string>(aliases["CountOfConsultants"]) == "C2Count");
    EXPECT_TRUE(std::get<std::string>(aliases["End1"]) == "EndDate");
    EXPECT_TRUE(std::get<std::string>(aliases["Start1"]) == "StartDate");
}

TEST(ColumnAliases, ColumnAliasesWithMultipleFunctions) {
    std::string query = R"SQL(
    SELECT a, sum(b) + sum(c) as alias1, custome_func(d) alias2 from aa, bb
    )SQL";
    Parser parser(query);
    EXPECT_EQ(parser.getTables(), std::vector<std::string>{"aa", "bb"});
    EXPECT_EQ(parser.getColumns(), std::vector<std::string>{"a", "b", "c", "d"});
    EXPECT_EQ(parser.getColumnAliasesNames(), std::vector<std::string>{"alias1", "alias2"});
    auto aliases = parser.getColumnAliases();
    EXPECT_TRUE(std::holds_alternative<std::vector<std::string>>(aliases["alias1"]));
    EXPECT_EQ(std::get<std::vector<std::string>>(aliases["alias1"]), std::vector<std::string>({"b", "c"}));
    EXPECT_TRUE(std::get<std::string>(aliases["alias2"]) == "d");
}

TEST(ColumnAliases, ColumnAliasesWithColumnsOperations) {
    std::string query = R"SQL(
    SELECT a, b + c - u as alias1, custome_func(d) alias2 from aa, bb
    )SQL";
    Parser parser(query);
    EXPECT_EQ(parser.getTables(), std::vector<std::string>{"aa", "bb"});
    EXPECT_EQ(parser.getColumns(), std::vector<std::string>{"a", "b", "c", "u", "d"});
    EXPECT_EQ(parser.getColumnAliasesNames(), std::vector<std::string>{"alias1", "alias2"});
    auto aliases = parser.getColumnAliases();
    EXPECT_TRUE(std::holds_alternative<std::vector<std::string>>(aliases["alias1"]));
    EXPECT_EQ(std::get<std::vector<std::string>>(aliases["alias1"]), std::vector<std::string>({"b", "c", "u"}));
    EXPECT_TRUE(std::get<std::string>(aliases["alias2"]) == "d");
}

TEST(ColumnAliases, ColumnAliasesWithRedundantBrackets) {
    std::string query = R"SQL(
    SELECT a, (b + c - u) as alias1, custome_func(d) alias2 from aa, bb order by alias1
    )SQL";
    Parser parser(query);
    EXPECT_EQ(parser.getTables(), std::vector<std::string>{"aa", "bb"});
    EXPECT_EQ(parser.getColumns(), std::vector<std::string>{"a", "b", "c", "u", "d"});
    EXPECT_EQ(parser.getColumnAliasesNames(), std::vector<std::string>{"alias1", "alias2"});
    auto aliases = parser.getColumnAliases();
    EXPECT_TRUE(std::holds_alternative<std::vector<std::string>>(aliases["alias1"]));
    EXPECT_EQ(std::get<std::vector<std::string>>(aliases["alias1"]), std::vector<std::string>({"b", "c", "u"}));
    EXPECT_TRUE(std::get<std::string>(aliases["alias2"]) == "d");
    // column_aliases_dict checks
    auto col_aliases_dict = parser.getColumnsDict(); // should be the dict grouped by section e.g. order_by, select
    EXPECT_EQ(col_aliases_dict["order_by"], std::vector<std::string>({"alias1"}));
    EXPECT_EQ(col_aliases_dict["select"], std::vector<std::string>({"alias1", "alias2"}));
    auto col_dict = parser.getColumnsDict();
    EXPECT_EQ(col_dict["order_by"], std::vector<std::string>({"b", "c", "u"}));
    EXPECT_EQ(col_dict["select"], std::vector<std::string>({"a", "b", "c", "u", "d"}));
}

// ... (implement the rest of the tests similarly for all file's functions)