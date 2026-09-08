package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.sql.*;

public class TestSqlite3 {

    @Test
    public void testSqliteInMemory() throws SQLException {
        Connection connection = DriverManager.getConnection("jdbc:sqlite::memory:");
        Statement stmt = connection.createStatement();
        stmt.executeUpdate("CREATE TABLE test (id INTEGER PRIMARY KEY, value TEXT)");
        stmt.executeUpdate("INSERT INTO test (value) VALUES ('hello')");
        ResultSet rs = stmt.executeQuery("SELECT value FROM test WHERE id=1");

        assertTrue(rs.next());
        assertEquals("hello", rs.getString("value"));

        stmt.close();
        connection.close();
    }
}