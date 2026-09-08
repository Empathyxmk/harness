package me.drakeet.floo;

import org.junit.Test;
import static org.junit.Assert.*;

public class ChainTest {

    private static class TestInterceptor implements Interceptor {
        boolean called = false;
        @Override
        public void intercept(Chain chain) {
            called = true;
        }
    }

    @Test
    public void testChainSetAndProceed() {
        Chain chain = new Chain();
        TestInterceptor interceptor = new TestInterceptor();
        chain.setInterceptor(interceptor);
        assertSame(interceptor, chain.getInterceptor());

        chain.proceed();
        assertTrue(interceptor.called);
    }

    @Test
    public void testChainCallback() {
        Chain chain = new Chain();
        final boolean[] called = {false};
        chain.setCallback(new Runnable() {
            @Override
            public void run() {
                called[0] = true;
            }
        });
        chain.callback();
        assertTrue(called[0]);
    }

    @Test
    public void testDefaultStates() {
        Chain chain = new Chain();
        assertNull(chain.getInterceptor());
    }
}