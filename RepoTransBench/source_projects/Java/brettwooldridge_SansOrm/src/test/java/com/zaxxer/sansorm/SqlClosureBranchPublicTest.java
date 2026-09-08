package com.zaxxer.sansorm;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import javax.sql.DataSource;

import static org.junit.Assert.*;

public class SqlClosureBranchPublicTest {
    private DataSourceStubPublic dataSource;

    @Before
    public void setup() {
        dataSource = new DataSourceStubPublic();
    }

    @After
    public void cleanup() {
        SqlClosure.setDefaultDataSource(null);
    }

    @Test(expected = RuntimeException.class)
    public void testDefaultConstructorThrowsIfNoDataSource_Public() {
        SqlClosure.setDefaultDataSource(null);
        new SqlClosure<Object>();
    }

    @Test
    public void testOtherConstructorsWithoutDefaultDataSource_Public() {
        SqlClosure<Object> c1 = new SqlClosure<>(dataSource);
        assertNotNull(c1);

        SqlClosure<Object> c2 = new SqlClosure<>(dataSource, "public_arg", 84);
        assertNotNull(c2);

        SqlClosure<Object> c3 = new SqlClosure<>(new SqlClosure<>(dataSource));
        assertNotNull(c3);

        SqlClosure<Object> c4 = new SqlClosure<>("x", "y");
        assertNotNull(c4);
    }

    @Test
    public void testSetDefaultDataSource_Public() {
        SqlClosure.setDefaultDataSource(dataSource);
        SqlClosure<?> c = new SqlClosure<Object>();
        assertNotNull(c);
    }

    // Stub class for minimal interface implementation (omit methods with java.sql.ShardingKey)
    static class DataSourceStubPublic implements DataSource {
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