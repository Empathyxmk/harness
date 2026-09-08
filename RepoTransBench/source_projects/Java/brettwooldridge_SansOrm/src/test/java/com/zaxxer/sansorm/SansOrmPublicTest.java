package com.zaxxer.sansorm;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import javax.sql.DataSource;
import javax.transaction.TransactionManager;
import javax.transaction.UserTransaction;

import static org.junit.Assert.*;

public class SansOrmPublicTest {

    private DataSourceStubPublic dataSource;
    private TransactionManagerStubPublic transactionManager;
    private UserTransactionStubPublic userTransaction;

    @Before
    public void setUp() {
        dataSource = new DataSourceStubPublic();
        transactionManager = new TransactionManagerStubPublic();
        userTransaction = new UserTransactionStubPublic();
        SansOrm.deinitialize();
    }

    @After
    public void tearDown() {
        SansOrm.deinitialize();
    }

    @Test
    public void testInitializeTxNone_Public() {
        DataSource result = SansOrm.initializeTxNone(dataSource);
        assertNotNull(result);
        assertEquals(dataSource, result);
    }

    @Test
    public void testInitializeTxSimple_Public() {
        DataSource result = SansOrm.initializeTxSimple(dataSource);
        assertNotNull(result);
    }

    @Test
    public void testInitializeTxCustom_Public() {
        DataSource result = SansOrm.initializeTxCustom(dataSource, transactionManager, userTransaction);
        assertEquals(dataSource, result);
    }

    @Test
    public void testDeinitialize_Public() {
        SansOrm.initializeTxCustom(dataSource, transactionManager, userTransaction);
        SansOrm.deinitialize();
    }

    // Minimal stub classes for interfaces required
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
    static class TransactionManagerStubPublic implements TransactionManager {
        public void begin() {}
        public void commit() {}
        public int getStatus() { return 0; }
        public void rollback() {}
        public void setRollbackOnly() {}
        public void setTransactionTimeout(int seconds) {}
        public javax.transaction.Transaction suspend() { return null; }
        public void resume(javax.transaction.Transaction tobj) {}
        public javax.transaction.Transaction getTransaction() { return null; }
    }
    static class UserTransactionStubPublic implements UserTransaction {
        public void begin() {}
        public void commit() {}
        public void rollback() {}
        public void setRollbackOnly() {}
        public void setTransactionTimeout(int seconds) {}
        public int getStatus() { return 0; }
    }
}