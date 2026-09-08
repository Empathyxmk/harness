package com.geektime.systrace;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;

public class LogPublicTest {

    private static class PublicTestLogImp implements Log.LogImp {
        boolean vCalled, iCalled, wCalled, dCalled, eCalled, errStackTraceCalled;
        String lastTag, lastMsg;
        Object[] lastObj;
        Throwable lastTr;
        String lastFormat;

        @Override
        public void v(String tag, String msg, Object... obj) {
            vCalled = true; lastTag = tag; lastMsg = msg; lastObj = obj;
        }

        @Override
        public void i(String tag, String msg, Object... obj) {
            iCalled = true; lastTag = tag; lastMsg = msg; lastObj = obj;
        }

        @Override
        public void w(String tag, String msg, Object... obj) {
            wCalled = true; lastTag = tag; lastMsg = msg; lastObj = obj;
        }

        @Override
        public void d(String tag, String msg, Object... obj) {
            dCalled = true; lastTag = tag; lastMsg = msg; lastObj = obj;
        }

        @Override
        public void e(String tag, String msg, Object... obj) {
            eCalled = true; lastTag = tag; lastMsg = msg; lastObj = obj;
        }

        @Override
        public void printErrStackTrace(String tag, Throwable tr, String format, Object... obj) {
            errStackTraceCalled = true; lastTag = tag; lastMsg = null; lastTr = tr; lastFormat = format; lastObj = obj;
        }
    }

    private Log.LogImp original;

    @Before
    public void setup() {
        original = Log.getImpl();
    }

    @After
    public void cleanup() {
        Log.setLogImp(original);
    }

    @Test
    public void testSetAndGetImplPublic() {
        PublicTestLogImp imp = new PublicTestLogImp();
        Log.setLogImp(imp);
        assertEquals(imp, Log.getImpl());
    }

    @Test
    public void testLogMethodsDelegateToImplPublic() {
        PublicTestLogImp imp = new PublicTestLogImp();
        Log.setLogImp(imp);

        Log.v("PUB", "Verbose log %d", 10);
        Log.i("PUB", "Info log");
        Log.w("PUB", "Warning %d", 24);
        Log.d("PUB", "Debug message");
        Log.e("PUB", "Error string %s", "oops");

        Throwable t = new IllegalArgumentException("public error");
        Log.printErrStackTrace("PUB", t, "formatting %s", "msg2");
        assertTrue(imp.vCalled);
        assertTrue(imp.iCalled);
        assertTrue(imp.wCalled);
        assertTrue(imp.dCalled);
        assertTrue(imp.eCalled);
        assertTrue(imp.errStackTraceCalled);
        assertEquals(t, imp.lastTr);
        assertEquals("PUB", imp.lastTag);
    }

    @Test
    public void testNullImplDoesNotThrowPublic() {
        Log.setLogImp(null);
        // Should simply not throw
        Log.v("PUB", "message");
        Log.d("PUB", "message");
        Log.i("PUB", "message");
        Log.w("PUB", "message");
        Log.e("PUB", "message");
        Log.printErrStackTrace("PUB", new Exception("public error"), "message");
    }
}