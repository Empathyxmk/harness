package com.dianping.zebra.dao;

import org.junit.jupiter.api.*;

import java.lang.reflect.Method;
import java.util.concurrent.Future;
import java.util.concurrent.atomic.AtomicReference;

import static org.junit.jupiter.api.Assertions.*;

public class AsyncMapperExecutorPublicTest {

    static class DummyMapper {
        public String repeat(String in) {
            return in + in;
        }
        public String throwsOtherError() {
            throw new IllegalStateException("fail!");
        }
    }

    @BeforeAll
    public static void setupExecutor() {
        AsyncMapperExecutor.init(2, 3, 2);
    }

    @AfterEach
    public void ensureExecutor() {
        AsyncMapperExecutor.init(2, 3, 2);
    }

    @Test
    public void testSubmitCallbackReturns() throws Exception {
        DummyMapper mapper = new DummyMapper();
        Method m = DummyMapper.class.getMethod("repeat", String.class);
        Future<?> f = AsyncMapperExecutor.submitCallback(mapper, m, new Object[]{"xyz"});
        assertEquals("xyzxyz", f.get());
    }

    @Test
    public void testExecuteRunnableSuccess() throws Exception {
        DummyMapper mapper = new DummyMapper();
        Method m = DummyMapper.class.getMethod("repeat", String.class);

        AtomicReference<Object> result = new AtomicReference<>();
        AtomicReference<Exception> error = new AtomicReference<>();
        AsyncDaoCallback<String> cb = new AsyncDaoCallback<String>() {
            @Override public void onSuccess(String resultStr) { result.set(resultStr); }
            @Override public void onException(Exception e) { error.set(e); }
        };

        AsyncMapperExecutor.executeRunnable(mapper, m, new Object[]{"bar"}, cb);

        Thread.sleep(200);

        assertEquals("barbar", result.get());
        assertNull(error.get());
    }

    @Test
    public void testExecuteRunnableThrows() throws Exception {
        DummyMapper mapper = new DummyMapper();
        Method m = DummyMapper.class.getMethod("throwsOtherError");

        AtomicReference<Object> result = new AtomicReference<>();
        AtomicReference<Exception> error = new AtomicReference<>();
        AsyncDaoCallback<String> cb = new AsyncDaoCallback<String>() {
            @Override public void onSuccess(String resultStr) { result.set(resultStr); }
            @Override public void onException(Exception e) { error.set(e); }
        };

        AsyncMapperExecutor.executeRunnable(mapper, m, null, cb);

        Thread.sleep(200);

        assertNull(result.get());
        assertNotNull(error.get());
        assertEquals("fail!", error.get().getCause().getMessage());
    }

    @Test
    public void testCheckNullThrows() {
        var field = assertDoesNotThrow(() -> AsyncMapperExecutor.class.getDeclaredField("executorService"));
        field.setAccessible(true);
        try {
            var prev = field.get(null);
            field.set(null, null);
            AsyncDaoException ex = assertThrows(AsyncDaoException.class,
                () -> AsyncMapperExecutor.submitCallback(new DummyMapper(),
                        DummyMapper.class.getMethod("repeat", String.class),
                        new Object[]{"xyz"}));
            assertEquals("AsyncMapperExecutor has not been init yet.", ex.getMessage());
            field.set(null, prev);
        } catch (Exception e) {
            fail(e);
        }
    }

    @Test
    public void testSetCorePoolSizeMethods() {
        AsyncMapperExecutor.setCorePoolSize(2);
        AsyncMapperExecutor.setMaximumPoolSize(3);
    }
}