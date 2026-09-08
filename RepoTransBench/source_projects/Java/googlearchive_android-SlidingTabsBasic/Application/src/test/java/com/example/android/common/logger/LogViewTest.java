package com.example.android.common.logger;

import android.content.Context;
import android.app.Activity;
import android.util.AttributeSet;
import org.junit.*;
import static org.mockito.Mockito.*;

public class LogViewTest {

    private static class DummyActivity extends Activity {
        private Runnable uiRunnable;
        @Override
        public void runOnUiThread(Runnable runnable) {
            this.uiRunnable = runnable;
            runnable.run(); // direct execution for test!
        }
    }

    private static class DummyContext extends DummyActivity implements Context {}

    @Test
    public void testConstructors() {
        Context ctx = mock(Context.class);
        AttributeSet attrs = mock(AttributeSet.class);

        LogView v1 = new LogView(ctx);
        LogView v2 = new LogView(ctx, attrs);
        LogView v3 = new LogView(ctx, attrs, 1);
        Assert.assertNotNull(v1);
        Assert.assertNotNull(v2);
        Assert.assertNotNull(v3);
    }

    @Test
    public void testAppendIfNotNullBehavior() {
        Context ctx = mock(Context.class);
        LogView v = new LogView(ctx);

        StringBuilder sb = new StringBuilder("start");
        StringBuilder sb2 = invokeAppendIfNotNull(v, sb, "add", ",");
        Assert.assertEquals("startadd,", sb2.toString());

        sb = new StringBuilder("x");
        sb2 = invokeAppendIfNotNull(v, sb, "", ",");
        Assert.assertEquals("x", sb2.toString());

        sb = new StringBuilder();
        sb2 = invokeAppendIfNotNull(v, sb, null, "|");
        Assert.assertEquals("", sb2.toString());
    }

    private StringBuilder invokeAppendIfNotNull(LogView v, StringBuilder sb, String add, String del) {
        try {
            java.lang.reflect.Method m = LogView.class.getDeclaredMethod("appendIfNotNull", StringBuilder.class, String.class, String.class);
            m.setAccessible(true);
            return (StringBuilder) m.invoke(v, sb, add, del);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    @Test
    public void testPrintlnFormatsAndAppends() {
        DummyActivity ctx = spy(new DummyActivity());
        LogView v = spy(new LogView(ctx));
        String[] output = {null};
        doAnswer(invocation -> {
            output[0] = (String) invocation.getArguments()[0];
            return null;
        }).when(v).appendToLog(any());

        v.println(android.util.Log.WARN, "tag1", "msg1", null);

        Assert.assertTrue(output[0].contains("WARN") && output[0].contains("tag1") && output[0].contains("msg1"));

        Throwable t = new RuntimeException("Test");
        v.println(android.util.Log.ERROR, "tag2", "msg2", t);
        Assert.assertTrue(output[0].contains("ERROR") && output[0].contains("msg2"));
        Assert.assertTrue(output[0].contains("RuntimeException"));

        // test mNext
        LogNode next = mock(LogNode.class);
        v.setNext(next);
        v.println(android.util.Log.INFO, "tagx", "msgx", null);
        verify(next).println(anyInt(), any(), any(), any());
    }

    @Test
    public void testSetAndGetNext() {
        Context ctx = mock(Context.class);
        LogView v = new LogView(ctx);
        Assert.assertNull(v.getNext());
        LogNode ln = mock(LogNode.class);
        v.setNext(ln);
        Assert.assertEquals(ln, v.getNext());
    }
}