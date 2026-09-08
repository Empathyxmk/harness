package com.dianping.zebra.dao;

import org.junit.jupiter.api.*;

import java.lang.reflect.Method;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Future;
import java.util.concurrent.atomic.AtomicReference;

import static org.junit.jupiter.api.Assertions.*;

public class AsyncMapperExecutorTest {

    static class DummyMapper {
        public String reverse(String in) {
            return new StringBuilder(in).reverse().toString();
        }
        public String throwsError() {
            throw new IllegalStateException("err!");
        }
    }

    @BeforeAll
    public static void setupExecutor() {
        AsyncMapperExecutor.init(1, 2, 2);
    }

    @AfterEach
    public void ensureExecutor() {
        // forcibly re-init after pool size mutation tests
        AsyncMapperExecutor.init(1, 2, 2);
    }

    @Test
    public void testSubmitCallbackReturns() throws Exception {
        DummyMapper mapper = new DummyMapper();
        Method m = DummyMapper.class.getMethod("reverse", String.class);
        Future<?> f = AsyncMapperExecutor.submitCallback(mapper, m, new Object[]{"abc"});
        assertEquals("cba", f.get());
    }

    @Test
    public void testExecuteRunnableSuccess() throws Exception {
        DummyMapper mapper = new DummyMapper();
        Method m = DummyMapper.class.getMethod("reverse", String.class);

        AtomicReference<Object> result = new AtomicReference<>();
        AtomicReference<Exception> error = new AtomicReference<>();
        AsyncDaoCallback<String> cb = new AsyncDaoCallback<String>() {
            @Override public void onSuccess(String resultStr) { result.set(resultStr); }
            @Override public void onException(Exception e) { error.set(e); }
        };

        AsyncMapperExecutor.executeRunnable(mapper, m, new Object[]{"foo"}, cb);

        Thread.sleep(200); // allow async thread to run

        assertEquals("oof", result.get());
        assertNull(error.get());
    }

    @Test
    public void testExecuteRunnableThrows() throws Exception {
        DummyMapper mapper = new DummyMapper();
        Method m = DummyMapper.class.getMethod("throwsError");

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
        assertEquals("err!", error.get().getCause().getMessage());
    }

    @Test
    public void testCheckNullThrows() {
        // forcibly remove executorService for test
        var field = assertDoesNotThrow(() -> AsyncMapperExecutor.class.getDeclaredField("executorService"));
        field.setAccessible(true);
        try {
            var prev = field.get(null);
            field.set(null, null);
            AsyncDaoException ex = assertThrows(AsyncDaoException.class,
                () -> AsyncMapperExecutor.submitCallback(new DummyMapper(),
                        DummyMapper.class.getMethod("reverse", String.class),
                        new Object[]{"abc"}));
            assertEquals("AsyncMapperExecutor has not been init yet.", ex.getMessage());
            field.set(null, prev); // restore
        } catch (Exception e) {
            fail(e);
        }
    }

    @Test
    public void testSetCorePoolSizeMethods() {
        AsyncMapperExecutor.setCorePoolSize(1);
        AsyncMapperExecutor.setMaximumPoolSize(2);
        // No assertion necessary - just branch coverage
    }
}