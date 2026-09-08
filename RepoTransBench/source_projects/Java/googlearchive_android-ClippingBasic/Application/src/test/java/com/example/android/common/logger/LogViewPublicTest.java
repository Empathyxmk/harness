package com.example.android.common.logger;

import android.content.Context;
import android.app.Activity;
import android.os.Looper;
import android.util.AttributeSet;

import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

import static org.junit.Assert.*;

public class LogViewPublicTest {

    static class DummyActivity extends Activity {
        boolean didRunOnUiThread = false;
        Runnable lastRunnable;

        @Override
        public void runOnUiThread(Runnable action) {
            didRunOnUiThread = true;
            lastRunnable = action;
            // Execute action for test purposes
            action.run();
        }
    }

    private DummyActivity dummyActivity;

    @Before
    public void setUp() {
        dummyActivity = new DummyActivity();
    }

    @Test
    public void testAppendIfNotNullPublic() {
        LogView view = new LogView(dummyActivity);

        StringBuilder sb = new StringBuilder();
        StringBuilder result = view.appendIfNotNull(sb, "xyz", ";");
        assertEquals("xyz;", result.toString());
        sb = new StringBuilder();
        result = view.appendIfNotNull(sb, null, "~");
        assertEquals("", result.toString());

        sb = new StringBuilder("y");
        result = view.appendIfNotNull(sb, "", "?");
        assertEquals("y", result.toString());
    }

    @Test
    public void testGetSetNextPublic() {
        LogView view = new LogView(dummyActivity);
        MessageOnlyLogFilter filter = new MessageOnlyLogFilter();
        view.setNext(filter);
        assertEquals(filter, view.getNext());
    }

    @Test
    public void testPrintlnFormatsAndRunsRunnablePublic() {
        LogView view = new LogView(dummyActivity);
        LogNode next = Mockito.mock(LogNode.class);
        view.setNext(next);

        Throwable tr = new RuntimeException("pubTest");
        view.println(android.util.Log.WARN, "publicTag", "publicMsg", tr);

        Mockito.verify(next).println(android.util.Log.WARN, "publicTag", "publicMsg", tr);

        // Must have executed the runnable via UI thread emulation
        assertTrue(dummyActivity.didRunOnUiThread);
    }
}