package com.dianping.zebra.dao;

import org.junit.jupiter.api.Test;

import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicReference;
import java.util.concurrent.*;

import static org.junit.jupiter.api.Assertions.*;

class AsyncDaoCallableExecutorPublicTest {

    static class DummyCallable {
        public int calc(int a, int b) {
            return a - b;
        }

        public int throwSomething() {
            throw new IllegalArgumentException("sub_fail");
        }
    }

    @Test
    void testCallableRunSuccess() throws Exception {
        DummyCallable inst = new DummyCallable();
        var method = DummyCallable.class.getMethod("calc", int.class, int.class);
        final AtomicReference<Object> output = new AtomicReference<>();
        final AtomicReference<Exception> err = new AtomicReference<>();

        AsyncDaoCallback<Integer> cb = new AsyncDaoCallback<Integer>() {
            public void onSuccess(Integer value) { output.set(value); }
            public void onException(Exception e) { err.set(e); }
        };

        AsyncDaoCallableExecutor<Integer> exec =
                new AsyncDaoCallableExecutor<>(inst, method, new Object[]{8, 3}, cb);
        Integer val = exec.call();

        assertEquals(5, val);
        assertNull(err.get());
        assertEquals(5, output.get());
    }

    @Test
    void testCallableThrowsException() throws Exception {
        DummyCallable inst = new DummyCallable();
        var method = DummyCallable.class.getMethod("throwSomething");
        final AtomicReference<Object> output = new AtomicReference<>();
        final AtomicReference<Exception> err = new AtomicReference<>();
        final AtomicBoolean exceptionFired = new AtomicBoolean(false);

        AsyncDaoCallback<Integer> cb = new AsyncDaoCallback<Integer>() {
            public void onSuccess(Integer value) { output.set(value); }
            public void onException(Exception e) {
                err.set(e);
                exceptionFired.set(true);
            }
        };

        AsyncDaoCallableExecutor<Integer> exec =
                new AsyncDaoCallableExecutor<>(inst, method, null, cb);
        Exception ex = assertThrows(Exception.class, exec::call);

        assertNull(output.get());
        assertTrue(exceptionFired.get());
        assertNotNull(err.get());
        assertEquals("sub_fail", err.get().getCause().getMessage());
    }
}