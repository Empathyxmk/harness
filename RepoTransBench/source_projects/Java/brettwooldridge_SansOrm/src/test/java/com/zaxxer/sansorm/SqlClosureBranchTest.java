package com.zaxxer.sansorm;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import javax.sql.DataSource;

import static org.junit.Assert.*;

public class SqlClosureBranchTest {
    private DataSourceStub dataSource;

    @Before
    public void setup() {
        dataSource = new DataSourceStub();
    }

    @After
    public void cleanup() {
        SqlClosure.setDefaultDataSource(null);
    }

    @Test(expected = RuntimeException.class)
    public void testDefaultConstructorThrowsIfNoDataSource() {
        SqlClosure.setDefaultDataSource(null);
        new SqlClosure<Object>();
    }

    @Test
    public void testOtherConstructorsWithoutDefaultDataSource() {
        SqlClosure<Object> c1 = new SqlClosure<>(dataSource);
        assertNotNull(c1);

        SqlClosure<Object> c2 = new SqlClosure<>(dataSource, "arg1", 42);
        assertNotNull(c2);

        SqlClosure<Object> c3 = new SqlClosure<>(new SqlClosure<>(dataSource));
        assertNotNull(c3);

        SqlClosure<Object> c4 = new SqlClosure<>("a", "b");
        assertNotNull(c4);
    }

    @Test
    public void testSetDefaultDataSource() {
        SqlClosure.setDefaultDataSource(dataSource);
        SqlClosure<?> c = new SqlClosure<Object>();
        assertNotNull(c);
    }

    // Stub class for minimal interface implementation (omit methods with java.sql.ShardingKey)
    static class DataSourceStub implements DataSource {
        public java.io.PrintWriter getLogWriter() { return null; }
        public void setLogWriter(java.io.PrintWriter out) {}
        public void setLoginTimeout(int seconds) {}
        public int getLoginTimeout() { return 0; }
        public java.util.logging.Logger getParentLogger() { return null; }
        public java.sql.Connection getConnection() { return null; }
        public java.sql.Connection getConnection(String username, String password) { return null; }
        public <T> T unwrap(Class<T> iface) { return null; }
        public boolean isWrapperFor(Class<?> iface) { return false; }
    }
}