package com.dianping.zebra.dao;

import org.junit.jupiter.api.Test;

import java.lang.reflect.Method;

import static org.junit.jupiter.api.Assertions.*;

class AsyncDaoCallableExecutorTest {

    static class DummyMapper {
        public int add(int a, int b) { return a + b; }
        public void throwError() { throw new RuntimeException("fail"); }
    }

    @Test
    void testCallNormal() throws Exception {
        DummyMapper map = new DummyMapper();
        Method m = DummyMapper.class.getMethod("add", int.class, int.class);

        AsyncDaoCallableExecutor exec = new AsyncDaoCallableExecutor(map, m, new Object[]{3, 4});
        Object result = exec.call();
        assertEquals(7, result);
    }

    @Test
    void testCallThrowsException() throws Exception {
        DummyMapper map = new DummyMapper();
        Method m = DummyMapper.class.getMethod("throwError");

        AsyncDaoCallableExecutor exec = new AsyncDaoCallableExecutor(map, m, null);

        Exception ex = assertThrows(Exception.class, exec::call);
        assertEquals("fail", ex.getCause().getMessage());
    }
}