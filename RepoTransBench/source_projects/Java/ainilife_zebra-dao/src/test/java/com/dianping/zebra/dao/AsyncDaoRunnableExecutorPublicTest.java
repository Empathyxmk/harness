package com.dianping.zebra.dao;

import org.junit.jupiter.api.Test;

import java.lang.reflect.Method;
import java.util.concurrent.atomic.AtomicReference;

import static org.junit.jupiter.api.Assertions.*;

class AsyncDaoRunnableExecutorPublicTest {

    static class DummyMapper {
        public String doOtherStuff(String input) { return new StringBuilder(input).reverse().toString(); }
        public void throwOtherError() { throw new RuntimeException("boom2!"); }
    }

    @Test
    void testRunSuccess() throws Exception {
        DummyMapper mapper = new DummyMapper();
        Method m = DummyMapper.class.getMethod("doOtherStuff", String.class);
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

        AsyncDaoRunnableExecutor<String> exec = new AsyncDaoRunnableExecutor<>(mapper, m, new Object[]{"world"}, cb);
        exec.run();

        assertNull(exceptionResult.get());
        assertEquals("dlrow", successResult.get());
    }

    @Test
    void testRunException() throws Exception {
        DummyMapper mapper = new DummyMapper();
        Method m = DummyMapper.class.getMethod("throwOtherError");
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
        assertEquals("boom2!", exceptionResult.get().getCause().getMessage());
    }
}