package com.example.android.common.logger;

import android.content.Context;
import android.app.Activity;
import android.util.AttributeSet;
import org.junit.*;
import static org.mockito.Mockito.*;

public class LogViewPublicTest {

    private static class DummyActivity extends Activity {
        private Runnable uiRunnable;
        @Override
        public void runOnUiThread(Runnable runnable) {
            this.uiRunnable = runnable;
            runnable.run(); // execute for test
        }
    }

    @Test
    public void testAllConstructors() {
        Context ctx = mock(Context.class, "publicCtx");
        AttributeSet attrs = mock(AttributeSet.class, "publicAttrs");

        LogView v1 = new LogView(ctx);
        LogView v2 = new LogView(ctx, attrs);
        LogView v3 = new LogView(ctx, attrs, 2);
        Assert.assertNotNull(v1);
        Assert.assertNotNull(v2);
        Assert.assertNotNull(v3);
    }

    @Test
    public void testAppendIfNotNullEdgeCases() {
        Context ctx = mock(Context.class, "publicCtx2");
        LogView v = new LogView(ctx);

        StringBuilder sb = new StringBuilder("public");
        StringBuilder sb2 = runAppendIfNotNull(v, sb, "append", "|");
        Assert.assertEquals("publicappend|", sb2.toString());

        sb = new StringBuilder("q");
        sb2 = runAppendIfNotNull(v, sb, "", "|");
        Assert.assertEquals("q", sb2.toString());

        sb = new StringBuilder();
        sb2 = runAppendIfNotNull(v, sb, null, ";");
        Assert.assertEquals("", sb2.toString());
    }

    private StringBuilder runAppendIfNotNull(LogView v, StringBuilder sb, String add, String del) {
        try {
            java.lang.reflect.Method m = LogView.class.getDeclaredMethod("appendIfNotNull", StringBuilder.class, String.class, String.class);
            m.setAccessible(true);
            return (StringBuilder) m.invoke(v, sb, add, del);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    @Test
    public void testPrintlnWithPublicData() {
        DummyActivity ctx = spy(new DummyActivity());
        LogView v = spy(new LogView(ctx));
        String[] catching = {null};
        doAnswer(invocation -> {
            catching[0] = (String) invocation.getArguments()[0];
            return null;
        }).when(v).appendToLog(any());

        v.println(android.util.Log.INFO, "tagPublic1", "msgInfo", null);
        Assert.assertTrue(catching[0].contains("INFO") && catching[0].contains("tagPublic1") && catching[0].contains("msgInfo"));

        Throwable t = new IllegalArgumentException("InvalidArg");
        v.println(android.util.Log.DEBUG, "tagPublic2", "msgDebug", t);
        Assert.assertTrue(catching[0].contains("DEBUG") && catching[0].contains("msgDebug"));
        Assert.assertTrue(catching[0].contains("IllegalArgumentException"));

        // Next node test
        LogNode next = mock(LogNode.class, "publicNext");
        v.setNext(next);
        v.println(android.util.Log.VERBOSE, "tagP", "msgP", null);
        verify(next).println(anyInt(), any(), any(), any());
    }

    @Test
    public void testSetGetNextNodePublic() {
        Context ctx = mock(Context.class, "publicCtx3");
        LogView v = new LogView(ctx);
        Assert.assertNull(v.getNext());
        LogNode ln = mock(LogNode.class, "publicLogNode");
        v.setNext(ln);
        Assert.assertSame(ln, v.getNext());
    }
}