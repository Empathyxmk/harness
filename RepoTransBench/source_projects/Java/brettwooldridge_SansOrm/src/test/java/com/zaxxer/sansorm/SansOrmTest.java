package com.zaxxer.sansorm;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import javax.sql.DataSource;
import javax.transaction.TransactionManager;
import javax.transaction.UserTransaction;

import static org.junit.Assert.*;

public class SansOrmTest {

    private DataSourceStub dataSource;
    private TransactionManagerStub transactionManager;
    private UserTransactionStub userTransaction;

    @Before
    public void setUp() {
        dataSource = new DataSourceStub();
        transactionManager = new TransactionManagerStub();
        userTransaction = new UserTransactionStub();
        SansOrm.deinitialize();
    }

    @After
    public void tearDown() {
        SansOrm.deinitialize();
    }

    @Test
    public void testInitializeTxNone() {
        DataSource result = SansOrm.initializeTxNone(dataSource);
        assertNotNull(result);
        assertEquals(dataSource, result);
    }

    @Test
    public void testInitializeTxSimple() {
        DataSource result = SansOrm.initializeTxSimple(dataSource);
        assertNotNull(result);
    }

    @Test
    public void testInitializeTxCustom() {
        DataSource result = SansOrm.initializeTxCustom(dataSource, transactionManager, userTransaction);
        assertEquals(dataSource, result);
    }

    @Test
    public void testDeinitialize() {
        SansOrm.initializeTxCustom(dataSource, transactionManager, userTransaction);
        SansOrm.deinitialize(); // Should reset state, no exceptions
    }

    // Minimal stub classes for interfaces required
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
    static class TransactionManagerStub implements TransactionManager {
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
    static class UserTransactionStub implements UserTransaction {
        public void begin() {}
        public void commit() {}
        public void rollback() {}
        public void setRollbackOnly() {}
        public void setTransactionTimeout(int seconds) {}
        public int getStatus() { return 0; }
    }
}