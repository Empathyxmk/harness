package com.example.android.common.logger;

import org.junit.*;

import static org.mockito.Mockito.*;

public class MessageOnlyLogFilterTest {

    @Test
    public void testMessageOnlyForwarded() {
        LogNode next = mock(LogNode.class);
        MessageOnlyLogFilter filter = new MessageOnlyLogFilter(next);

        filter.println(Log.WARN, "Tag", "Message", new RuntimeException("err"));

        verify(next).println(eq(Log.NONE), isNull(), eq("Message"), isNull());
    }

    @Test
    public void testNoNextDoesNothing() {
        MessageOnlyLogFilter filter = new MessageOnlyLogFilter();
        // Should not throw and since next is null, nothing happens
        filter.println(Log.ERROR, "tag", "sample", null);
    }

    @Test
    public void testSetGetNext() {
        MessageOnlyLogFilter filter = new MessageOnlyLogFilter();
        Assert.assertNull(filter.getNext());
        LogNode dummy = mock(LogNode.class);
        filter.setNext(dummy);
        Assert.assertEquals(dummy, filter.getNext());
    }
}