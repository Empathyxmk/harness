package com.example.android.common.logger;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class MessageOnlyLogFilterTest {

    static class RecordingNode implements LogNode {
        public int lastPriority = Integer.MIN_VALUE;
        public String lastTag = "zzz";
        public String lastMsg = "uuu";
        public Throwable lastTr;

        @Override
        public void println(int priority, String tag, String msg, Throwable tr) {
            this.lastPriority = priority;
            this.lastTag = tag;
            this.lastMsg = msg;
            this.lastTr = tr;
        }
    }

    private MessageOnlyLogFilter filter;
    private RecordingNode recorder;

    @Before
    public void setup() {
        recorder = new RecordingNode();
        filter = new MessageOnlyLogFilter();
        filter.setNext(recorder);
    }

    @Test
    public void testPrintlnFiltersToMessageOnly() {
        filter.println(Log.INFO, "TAG", "hellomsg", new Exception("should not propagate"));
        assertEquals(Log.NONE, recorder.lastPriority);
        assertNull(recorder.lastTag);
        assertEquals("hellomsg", recorder.lastMsg);
        assertNull(recorder.lastTr);
    }

    @Test
    public void testConstructorWithNext() {
        MessageOnlyLogFilter f2 = new MessageOnlyLogFilter(recorder);
        assertEquals(recorder, f2.getNext());
    }

    @Test
    public void testSetAndGetNext() {
        MessageOnlyLogFilter f3 = new MessageOnlyLogFilter();
        f3.setNext(recorder);
        assertEquals(recorder, f3.getNext());
    }

    @Test
    public void testNullNextDoesNothing() {
        MessageOnlyLogFilter f4 = new MessageOnlyLogFilter();
        // Should not throw
        f4.println(Log.ERROR, "x", "yz", null);
    }
}