package com.example.android.common.logger;

import android.content.Context;
import android.app.Activity;
import android.os.Looper;
import android.util.AttributeSet;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;

import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;

import static org.junit.Assert.*;

public class LogViewTest {

    static class DummyActivity extends Activity {
        boolean didRunOnUiThread = false;
        Runnable lastRunnable;

        @Override
        public void runOnUiThread(Runnable action) {
            didRunOnUiThread = true;
            lastRunnable = action;
            // Run it immediately for test purposes
            action.run();
        }
    }

    private DummyActivity dummyActivity;

    @Before
    public void setUp() {
        dummyActivity = new DummyActivity();
    }

    @Test
    public void testAppendIfNotNullBehavior() {
        LogView view = new LogView(dummyActivity);

        StringBuilder sb = new StringBuilder();
        StringBuilder result = view.appendIfNotNull(sb, "abc", ",");
        assertEquals("abc,", result.toString());
        sb = new StringBuilder();
        result = view.appendIfNotNull(sb, null, "|");
        assertEquals("", result.toString());

        sb = new StringBuilder("x");
        // length 0 disables delimiter
        result = view.appendIfNotNull(sb, "", "|");
        assertEquals("x", result.toString());
    }

    @Test
    public void testGetSetNext() {
        LogView view = new LogView(dummyActivity);
        MessageOnlyLogFilter filter = new MessageOnlyLogFilter();
        view.setNext(filter);
        assertEquals(filter, view.getNext());
    }

    @Test
    public void testPrintlnFormatsAndRunsRunnable() {
        LogView view = new LogView(dummyActivity);
        LogNode next = Mockito.mock(LogNode.class);
        view.setNext(next);

        Throwable tr = new Exception("e");
        view.println(android.util.Log.INFO, "tag", "msg", tr);

        // Verify that the next LogNode is called with the same params
        Mockito.verify(next).println(android.util.Log.INFO, "tag", "msg", tr);

        // did run on UI thread and appended text
        assertTrue(dummyActivity.didRunOnUiThread);
        // There should not be NPE here.
    }
}