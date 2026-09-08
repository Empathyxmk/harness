from sql_metadata import Parser


def test_column_aliases_with_subquery_public():
    query = """
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
    """
    parser = Parser(query)
    assert parser.tables == ["employee_report"]
    assert parser.subqueries_names == ["sub2", "sub"]
    assert parser.subqueries == {
        "sub": "SELECT count(EmpID) as Cnt, UserSource, month(Start2) MStart, "
        "month(End2) MEnd from (SELECT EmployeeID as EmpID, UserSource, "
        "JoinDate as Start2, LeaveDate as End2 from employee_report) sub2 "
        "group by 2, 3, 4",
        "sub2": "SELECT EmployeeID as EmpID, UserSource, JoinDate as Start2, LeaveDate "
        "as End2 from employee_report",
    }
    assert parser.columns == [
        "JoinDate",
        "UserSource",
        "EmployeeID",
        "JoinDate",
        "LeaveDate",
        "employee_report.UserSource",
    ]
    assert parser.columns_aliases_names == [
        "TimeAgg",
        "Cnt",
        "MStart",
        "MEnd",
        "EmpID",
        "EmpCount",
    ]
    assert parser.columns_aliases == {
        "TimeAgg": "JoinDate",
        "EmpID": "EmployeeID",
        "Cnt": "EmpID",
        "EmpCount": "Cnt",
        "MEnd": "LeaveDate",
        "MStart": "JoinDate",
    }


def test_column_aliases_with_multiple_functions_public():
    query = """
    SELECT x, avg(y) + avg(z) as public_alias1, special_func(w) public_alias2 from xx, yy
    """
    parser = Parser(query)
    assert parser.tables == ["xx", "yy"]
    assert parser.columns == ["x", "y", "z", "w"]
    assert parser.columns_aliases_names == ["public_alias1", "public_alias2"]
    assert parser.columns_aliases == {"public_alias1": ["y", "z"], "public_alias2": "w"}


def test_column_aliases_with_columns_operations_public():
    query = """
    SELECT i, j * k / m as pa1, custom_fun(l) pa2 from ta, tb
    """
    parser = Parser(query)
    assert parser.tables == ["ta", "tb"]
    assert parser.columns == ["i", "j", "k", "m", "l"]
    assert parser.columns_aliases_names == ["pa1", "pa2"]
    assert parser.columns_aliases == {"pa1": ["j", "k", "m"], "pa2": "l"}


def test_column_aliases_with_redundant_brackets_public():
    query = """
    SELECT p, (q * r / s) as ra1, some_func(t) ra2 from table1, table2 order by ra1
    """
    parser = Parser(query)
    assert parser.tables == ["table1", "table2"]
    assert parser.columns == ["p", "q", "r", "s", "t"]
    assert parser.columns_aliases_names == ["ra1", "ra2"]
    assert parser.columns_aliases == {"ra1": ["q", "r", "s"], "ra2": "t"}
    assert parser.columns_aliases_dict == {
        "order_by": ["ra1"],
        "select": ["ra1", "ra2"],
    }
    assert parser.columns_dict == {
        "order_by": ["q", "r", "s"],
        "select": ["p", "q", "r", "s", "t"],
    }


def test_mutiple_functions_public():
    parser = Parser(
        "SELECT sum(val1) + max(val2) + min(val3)"
        "+ sum(distinct val4) + another_func(val5) as final_result from one"
    )
    assert parser.columns == ["val1", "val2", "val3", "val4", "val5"]
    assert parser.columns_aliases_names == ["final_result"]
    assert parser.columns_aliases == {"final_result": ["val1", "val2", "val3", "val4", "val5"]}


def test_cast_in_where_public():
    parser = Parser(
        "SELECT sum(e) as some_result, pk as aliasX FROM test1 where cast(f as bigint) < aliasX"
    )
    assert parser.columns_aliases_names == ["some_result", "aliasX"]
    assert parser.columns_aliases == {"some_result": "e", "aliasX": "pk"}
    assert parser.columns_aliases_dict == {"select": ["some_result", "aliasX"], "where": ["aliasX"]}


def test_cast_in_select_public():
    parser = Parser("select CAST(data as STRING) as data_string from sometable")
    assert parser.columns_aliases_names == ["data_string"]
    assert parser.columns_aliases == {"data_string": "data"}
    assert parser.columns_aliases_dict == {"select": ["data_string"]}


def test_convert_in_select_public():
    parser = Parser(
        "SELECT CONVERT(utf8_col USING latin1) as public_alias FROM utf8_table;"
    )
    assert parser.columns_aliases_names == ["public_alias"]
    assert parser.columns_aliases == {"public_alias": "utf8_col"}
    assert parser.columns_aliases_dict == {"select": ["public_alias"]}


def test_convert_in_join_public():
    parser = Parser(
        "SELECT u1.c1, u2.c2, CONVERT(u1.c2 USING latin1) FROM utf8_table u1 "
        "left join utf16_table u2 "
        "on CONVERT(u1.utf8_col USING latin1) = "
        "CONVERT(u2.utf8_col USING latin1) "
        "left join utf32_table u3 using (c1, c2);"
    )
    assert parser.columns == [
        "utf8_table.c1",
        "utf16_table.c2",
        "utf8_table.c2",
        "utf8_table.utf8_col",
        "utf16_table.utf8_col",
        "c1",
        "c2",
    ]
    assert parser.columns_dict == {
        "join": [
            "utf8_table.utf8_col",
            "utf16_table.utf8_col",
            "c1",
            "c2",
        ],
        "select": ["utf8_table.c1", "utf16_table.c2", "utf8_table.c2"],
    }