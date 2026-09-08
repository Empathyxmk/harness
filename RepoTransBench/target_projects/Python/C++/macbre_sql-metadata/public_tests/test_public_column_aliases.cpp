#include <gtest/gtest.h>
#include "parser.h"

using namespace sql_metadata;

TEST(PublicColumnAliases, ColumnAliasesWithSubqueryPublic) {
    std::string query = R"SQL(
    SELECT month(JoinDate) as                         TimeAgg,
       UserSource,
       (SELECT sum(Cnt)
        from (SELECT count(EmpID) as Cnt, UserSource,
        month(Start2) MStart, month(End2) MEnd
              from (
                       SELECT EmployeeID as EmpID, UserSource, JoinDate as Start2,
                       LeaveDate as End2
                       from employee_report
                   ) sub2
              group by 2, 3, 4) sub
        where MStart <= month(JoinDate)
          and MEnd >= month(JoinDate)
          and sub.UserSource = main.UserSource) EmpCount
FROM employee_report main
where JoinDate >= last_day(date_add(now(), interval -6 month))
group by 1, 2
order by 1, 2;
    )SQL";
    Parser parser(query);
    EXPECT_EQ(parser.getTables(), std::vector<std::string>{"employee_report"});
    EXPECT_EQ(parser.getSubqueryNames(), std::vector<std::string>{"sub2", "sub"});
    std::map<std::string, std::string> expected_subqueries = {
        {"sub", "SELECT count(EmpID) as Cnt, UserSource, month(Start2) MStart, month(End2) MEnd from (SELECT EmployeeID as EmpID, UserSource, JoinDate as Start2, LeaveDate as End2 from employee_report) sub2 group by 2, 3, 4"},
        {"sub2", "SELECT EmployeeID as EmpID, UserSource, JoinDate as Start2, LeaveDate as End2 from employee_report"}
    };
    EXPECT_EQ(parser.getSubqueries(), expected_subqueries);
    EXPECT_EQ(parser.getColumns(), (std::vector<std::string>{"JoinDate", "UserSource", "EmployeeID", "JoinDate", "LeaveDate", "employee_report.UserSource"}));
    EXPECT_EQ(parser.getColumnAliasesNames(), std::vector<std::string>{"TimeAgg", "Cnt", "MStart", "MEnd", "EmpID", "EmpCount"});
    auto aliases = parser.getColumnAliases();
    EXPECT_TRUE(std::get<std::string>(aliases["TimeAgg"]) == "JoinDate");
    EXPECT_TRUE(std::get<std::string>(aliases["EmpID"]) == "EmployeeID");
    EXPECT_TRUE(std::get<std::string>(aliases["Cnt"]) == "EmpID");
    EXPECT_TRUE(std::get<std::string>(aliases["EmpCount"]) == "Cnt");
    EXPECT_TRUE(std::get<std::string>(aliases["MEnd"]) == "LeaveDate");
    EXPECT_TRUE(std::get<std::string>(aliases["MStart"]) == "JoinDate");
}

// ...similarly for remaining public test functions from the file.