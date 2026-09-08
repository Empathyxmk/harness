package com.dianping.zebra.dao;

import org.junit.jupiter.api.Test;

import java.lang.reflect.Method;
import java.util.concurrent.atomic.AtomicReference;

import static org.junit.jupiter.api.Assertions.*;

class AsyncDaoRunnableExecutorTest {

    static class DummyMapper {
        public String doStuff(String input) { return input.toUpperCase(); }
        public void throwError() { throw new RuntimeException("boom!"); }
    }

    @Test
    void testRunSuccess() throws Exception {
        DummyMapper mapper = new DummyMapper();
        Method m = DummyMapper.class.getMethod("doStuff", String.class);
        AtomicReference<Object> successResult = new AtomicReference<>();
        AtomicReference<Exception> exceptionResult = new AtomicReference<>();

        AsyncDaoCallback<String> cb = new AsyncDaoCallback<String>() {
            @Override
            public void onSuccess(String result) {
                successResult.set(result);
            }
            @Override
            public void onException(Exception e) {
                exceptionResult.set(e);
            }
        };

        AsyncDaoRunnableExecutor<String> exec = new AsyncDaoRunnableExecutor<>(mapper, m, new Object[]{"hello"}, cb);
        exec.run();

        assertNull(exceptionResult.get());
        assertEquals("HELLO", successResult.get());
    }

    @Test
    void testRunException() throws Exception {
        DummyMapper mapper = new DummyMapper();
        Method m = DummyMapper.class.getMethod("throwError");
        AtomicReference<Object> successResult = new AtomicReference<>();
        AtomicReference<Exception> exceptionResult = new AtomicReference<>();

        AsyncDaoCallback<String> cb = new AsyncDaoCallback<String>() {
            @Override
            public void onSuccess(String result) {
                successResult.set(result);
            }
            @Override
            public void onException(Exception e) {
                exceptionResult.set(e);
            }
        };

        AsyncDaoRunnableExecutor<String> exec = new AsyncDaoRunnableExecutor<>(mapper, m, null, cb);
        exec.run();

        assertNull(successResult.get());
        assertNotNull(exceptionResult.get());
        assertEquals("boom!", exceptionResult.get().getCause().getMessage());
    }
}