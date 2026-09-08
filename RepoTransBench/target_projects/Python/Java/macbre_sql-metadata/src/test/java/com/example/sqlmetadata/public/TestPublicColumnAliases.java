package com.example.sqlmetadata.public;

import com.example.sqlmetadata.Parser;
import org.junit.jupiter.api.Test;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Translated from public_tests/test_public_column_aliases.py
 */
public class TestPublicColumnAliases {

    @Test
    public void testColumnAliasesWithSubqueryPublic() {
        String query = """
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
        """;
        Parser parser = new Parser(query);
        assertEquals(List.of("employee_report"), parser.getTables());
        assertEquals(List.of("sub2", "sub"), parser.getSubqueriesNames());
        Map<String, String> expectedSubs = new HashMap<>();
        expectedSubs.put("sub", "SELECT count(EmpID) as Cnt, UserSource, month(Start2) MStart, "
                + "month(End2) MEnd from (SELECT EmployeeID as EmpID, UserSource, "
                + "JoinDate as Start2, LeaveDate as End2 from employee_report) sub2 "
                + "group by 2, 3, 4");
        expectedSubs.put("sub2", "SELECT EmployeeID as EmpID, UserSource, JoinDate as Start2, LeaveDate "
                + "as End2 from employee_report");
        assertEquals(expectedSubs, parser.getSubqueries());
        assertEquals(List.of(
                "JoinDate",
                "UserSource",
                "EmployeeID",
                "JoinDate",
                "LeaveDate",
                "employee_report.UserSource"
        ), parser.getColumns());
        List<String> expectedAliasNames = List.of("TimeAgg", "Cnt", "MStart", "MEnd", "EmpID", "EmpCount");
        assertEquals(expectedAliasNames, parser.getColumnsAliasesNames());
        Map<String, Object> expectedAliases = new HashMap<>();
        expectedAliases.put("TimeAgg", "JoinDate");
        expectedAliases.put("EmpID", "EmployeeID");
        expectedAliases.put("Cnt", "EmpID");
        expectedAliases.put("EmpCount", "Cnt");
        expectedAliases.put("MEnd", "LeaveDate");
        expectedAliases.put("MStart", "JoinDate");
        assertEquals(expectedAliases, parser.getColumnsAliases());
    }

    @Test
    public void testColumnAliasesWithMultipleFunctionsPublic() {
        String query = """
        SELECT x, avg(y) + avg(z) as public_alias1, special_func(w) public_alias2 from xx, yy
        """;
        Parser parser = new Parser(query);
        assertEquals(List.of("xx", "yy"), parser.getTables());
        assertEquals(List.of("x", "y", "z", "w"), parser.getColumns());
        assertEquals(List.of("public_alias1", "public_alias2"), parser.getColumnsAliasesNames());
        Map<String, Object> expectedAliases = new HashMap<>();
        expectedAliases.put("public_alias1", List.of("y", "z"));
        expectedAliases.put("public_alias2", "w");
        assertEquals(expectedAliases, parser.getColumnsAliases());
    }

    @Test
    public void testColumnAliasesWithColumnsOperationsPublic() {
        String query = """
        SELECT i, j * k / m as pa1, custom_fun(l) pa2 from ta, tb
        """;
        Parser parser = new Parser(query);
        assertEquals(List.of("ta", "tb"), parser.getTables());
        assertEquals(List.of("i", "j", "k", "m", "l"), parser.getColumns());
        assertEquals(List.of("pa1", "pa2"), parser.getColumnsAliasesNames());
        Map<String, Object> expectedAliases = new HashMap<>();
        expectedAliases.put("pa1", List.of("j", "k", "m"));
        expectedAliases.put("pa2", "l");
        assertEquals(expectedAliases, parser.getColumnsAliases());
    }

    @Test
    public void testColumnAliasesWithRedundantBracketsPublic() {
        String query = """
        SELECT p, (q * r / s) as ra1, some_func(t) ra2 from table1, table2 order by ra1
        """;
        Parser parser = new Parser(query);
        assertEquals(List.of("table1", "table2"), parser.getTables());
        assertEquals(List.of("p", "q", "r", "s", "t"), parser.getColumns());
        assertEquals(List.of("ra1", "ra2"), parser.getColumnsAliasesNames());
        Map<String, Object> expectedAliases = new HashMap<>();
        expectedAliases.put("ra1", List.of("q", "r", "s"));
        expectedAliases.put("ra2", "t");
        assertEquals(expectedAliases, parser.getColumnsAliases());
        Map<String, List<String>> expectedColumnsAliasesDict = new HashMap<>();
        expectedColumnsAliasesDict.put("order_by", List.of("ra1"));
        expectedColumnsAliasesDict.put("select", List.of("ra1", "ra2"));
        assertEquals(expectedColumnsAliasesDict, parser.getColumnsAliasesDict());
        Map<String, List<String>> expectedColumnsDict = new HashMap<>();
        expectedColumnsDict.put("order_by", List.of("q", "r", "s"));
        expectedColumnsDict.put("select", List.of("p", "q", "r", "s", "t"));
        assertEquals(expectedColumnsDict, parser.getColumnsDict());
    }

    @Test
    public void testMutipleFunctionsPublic() {
        Parser parser = new Parser(
                "SELECT sum(val1) + max(val2) + min(val3)"
                        + "+ sum(distinct val4) + another_func(val5) as final_result from one"
        );
        assertEquals(List.of("val1", "val2", "val3", "val4", "val5"), parser.getColumns());
        assertEquals(List.of("final_result"), parser.getColumnsAliasesNames());
        Map<String, Object> expectedAliases = new HashMap<>();
        expectedAliases.put("final_result", List.of("val1", "val2", "val3", "val4", "val5"));
        assertEquals(expectedAliases, parser.getColumnsAliases());
    }

    @Test
    public void testCastInWherePublic() {
        Parser parser = new Parser(
                "SELECT sum(e) as some_result, pk as aliasX FROM test1 where cast(f as bigint) < aliasX"
        );
        assertEquals(List.of("some_result", "aliasX"), parser.getColumnsAliasesNames());
        Map<String, Object> expectedAliases = new HashMap<>();
        expectedAliases.put("some_result", "e");
        expectedAliases.put("aliasX", "pk");
        assertEquals(expectedAliases, parser.getColumnsAliases());
        Map<String, List<String>> expectedColumnsAliasesDict = new HashMap<>();
        expectedColumnsAliasesDict.put("select", List.of("some_result", "aliasX"));
        expectedColumnsAliasesDict.put("where", List.of("aliasX"));
        assertEquals(expectedColumnsAliasesDict, parser.getColumnsAliasesDict());
    }

    @Test
    public void testCastInSelectPublic() {
        Parser parser = new Parser("select CAST(data as STRING) as data_string from sometable");
        assertEquals(List.of("data_string"), parser.getColumnsAliasesNames());
        Map<String, Object> expectedAliases = new HashMap<>();
        expectedAliases.put("data_string", "data");
        assertEquals(expectedAliases, parser.getColumnsAliases());
        Map<String, List<String>> expectedColumnsAliasesDict = new HashMap<>();
        expectedColumnsAliasesDict.put("select", List.of("data_string"));
        assertEquals(expectedColumnsAliasesDict, parser.getColumnsAliasesDict());
    }

    @Test
    public void testConvertInSelectPublic() {
        Parser parser = new Parser(
                "SELECT CONVERT(utf8_col USING latin1) as public_alias FROM utf8_table;"
        );
        assertEquals(List.of("public_alias"), parser.getColumnsAliasesNames());
        Map<String, Object> expectedAliases = new HashMap<>();
        expectedAliases.put("public_alias", "utf8_col");
        assertEquals(expectedAliases, parser.getColumnsAliases());
        Map<String, List<String>> expectedColumnsAliasesDict = new HashMap<>();
        expectedColumnsAliasesDict.put("select", List.of("public_alias"));
        assertEquals(expectedColumnsAliasesDict, parser.getColumnsAliasesDict());
    }

    @Test
    public void testConvertInJoinPublic() {
        Parser parser = new Parser(
                "SELECT u1.c1, u2.c2, CONVERT(u1.c2 USING latin1) FROM utf8_table u1 "
                        + "left join utf16_table u2 "
                        + "on CONVERT(u1.utf8_col USING latin1) = "
                        + "CONVERT(u2.utf8_col USING latin1) "
                        + "left join utf32_table u3 using (c1, c2);"
        );
        assertEquals(List.of(
                "utf8_table.c1",
                "utf16_table.c2",
                "utf8_table.c2",
                "utf8_table.utf8_col",
                "utf16_table.utf8_col",
                "c1",
                "c2"
        ), parser.getColumns());
        Map<String, List<String>> expectedColumnsDict = new HashMap<>();
        expectedColumnsDict.put("join", List.of(
                "utf8_table.utf8_col",
                "utf16_table.utf8_col",
                "c1",
                "c2"
        ));
        expectedColumnsDict.put("select", List.of(
                "utf8_table.c1", "utf16_table.c2", "utf8_table.c2"
        ));
        assertEquals(expectedColumnsDict, parser.getColumnsDict());
    }
}