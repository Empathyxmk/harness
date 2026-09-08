package com.github.davidmoten.geo.db;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

import java.sql.*;

public class DatabasePublicTest {

    @Test
    public void testCreateTableAndInsertSelectDifferentData() throws SQLException {
        // Use in-memory database for isolation
        Connection conn = DriverManager.getConnection("jdbc:sqlite::memory:");
        try (Statement s = conn.createStatement()) {
            s.execute("CREATE TABLE foo (id INTEGER PRIMARY KEY, bar TEXT)");
            s.execute("INSERT INTO foo (bar) VALUES ('PublicFoo')");
        }
        try (PreparedStatement ps = conn.prepareStatement("SELECT bar FROM foo WHERE id=?")) {
            ps.setInt(1, 1);
            ResultSet rs = ps.executeQuery();
            assertTrue(rs.next());
            assertEquals("PublicFoo", rs.getString(1));
        }
        conn.close();
    }

    @Test
    public void testInsertAndCountRowsDifferent() throws SQLException {
        Connection conn = DriverManager.getConnection("jdbc:sqlite::memory:");
        try (Statement s = conn.createStatement()) {
            s.execute("CREATE TABLE baz (id INTEGER PRIMARY KEY, value INTEGER)");
            for (int i = 100; i < 105; i++) {
                s.execute("INSERT INTO baz (value) VALUES (" + i + ")");
            }
        }
        try (PreparedStatement ps = conn.prepareStatement("SELECT COUNT(*) FROM baz")) {
            ResultSet rs = ps.executeQuery();
            assertTrue(rs.next());
            assertEquals(5, rs.getInt(1));
        }
        conn.close();
    }
}