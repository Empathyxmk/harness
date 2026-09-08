package com.geektime.systrace;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;

public class LogTest {

    private static class TestLogImp implements Log.LogImp {
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
    public void testSetAndGetImpl() {
        TestLogImp imp = new TestLogImp();
        Log.setLogImp(imp);
        assertEquals(imp, Log.getImpl());
    }

    @Test
    public void testLogMethodsDelegateToImpl() {
        TestLogImp imp = new TestLogImp();
        Log.setLogImp(imp);

        Log.v("TAG", "Ver msg %d", 1);
        Log.i("TAG", "Info msg");
        Log.w("TAG", "Warn %d", 42);
        Log.d("TAG", "Dbg");
        Log.e("TAG", "Err %s", "msg");

        Throwable t = new RuntimeException("err");
        Log.printErrStackTrace("TAG", t, "format %s", "err");
        assertTrue(imp.vCalled);
        assertTrue(imp.iCalled);
        assertTrue(imp.wCalled);
        assertTrue(imp.dCalled);
        assertTrue(imp.eCalled);
        assertTrue(imp.errStackTraceCalled);
        assertEquals(t, imp.lastTr);
        assertEquals("TAG", imp.lastTag);
    }

    @Test
    public void testNullImplDoesNotThrow() {
        Log.setLogImp(null);
        // Should simply not throw
        Log.v("TAG", "msg");
        Log.d("TAG", "msg");
        Log.i("TAG", "msg");
        Log.w("TAG", "msg");
        Log.e("TAG", "msg");
        Log.printErrStackTrace("TAG", new Exception("err"), "msg");
    }
}