package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.sql.*;

public class TestPublicSqlite3 {

    @Test
    public void testSqliteInsert() throws SQLException {
        Connection conn = DriverManager.getConnection("jdbc:sqlite::memory:");
        Statement stm = conn.createStatement();
        stm.executeUpdate("CREATE TABLE foo (bar TEXT)");
        stm.executeUpdate("INSERT INTO foo (bar) VALUES ('baz')");
        ResultSet rs = stm.executeQuery("SELECT bar FROM foo");
        assertTrue(rs.next());
        assertEquals("baz", rs.getString("bar"));
        stm.close();
        conn.close();
    }
}