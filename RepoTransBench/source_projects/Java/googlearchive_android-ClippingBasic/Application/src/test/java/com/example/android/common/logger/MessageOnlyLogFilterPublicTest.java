package com.example.android.common.logger;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class MessageOnlyLogFilterPublicTest {

    static class RecordingNode implements LogNode {
        public int lastPriority = Integer.MAX_VALUE;
        public String lastTag = "abc";
        public String lastMsg = "zzz";
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
    public void testPrintlnFiltersToMessageOnlyPublic() {
        filter.println(Log.WARN, "PUBTAG", "public message", new Exception("not seen"));
        assertEquals(Log.NONE, recorder.lastPriority);
        assertNull(recorder.lastTag);
        assertEquals("public message", recorder.lastMsg);
        assertNull(recorder.lastTr);
    }

    @Test
    public void testConstructorWithNextPublic() {
        MessageOnlyLogFilter f2 = new MessageOnlyLogFilter(recorder);
        assertEquals(recorder, f2.getNext());
    }

    @Test
    public void testSetAndGetNextPublic() {
        MessageOnlyLogFilter f3 = new MessageOnlyLogFilter();
        f3.setNext(recorder);
        assertEquals(recorder, f3.getNext());
    }

    @Test
    public void testNullNextDoesNothingPublic() {
        MessageOnlyLogFilter f4 = new MessageOnlyLogFilter();
        // Should not throw
        f4.println(Log.VERBOSE, "v", "pqrs", null);
    }
}