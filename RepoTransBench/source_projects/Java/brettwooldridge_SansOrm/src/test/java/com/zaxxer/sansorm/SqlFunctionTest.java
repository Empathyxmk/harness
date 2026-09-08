package com.zaxxer.sansorm;

import org.junit.Test;

import java.sql.Connection;
import java.sql.SQLException;

import static org.junit.Assert.*;

public class SqlFunctionTest {
    @Test
    public void testSqlFunctionExecute() throws SQLException {
        SqlFunction<String> function = new SqlFunction<String>() {
            @Override
            public String execute(Connection connection) throws SQLException {
                return "ok";
            }
        };

        assertEquals("ok", function.execute(null));
    }

    @Test(expected = SQLException.class)
    public void testSqlFunctionExecuteThrows() throws SQLException {
        SqlFunction<Void> function = c -> { throw new SQLException("fail"); };
        function.execute(null);
    }
}