package com.example.android.common.logger;

import org.junit.*;

import static org.mockito.Mockito.*;

public class MessageOnlyLogFilterPublicTest {

    @Test
    public void testFiltersMessageOnlyDifferentInput() {
        MessageOnlyLogFilter filter = new MessageOnlyLogFilter();
        LogNode child = mock(LogNode.class, "publicChild");
        filter.setNext(child);

        filter.println(99, "PublicTAG", "HelloWorldMsg", null);
        // Should forward only the message string as tag and exception are not relevant to filter
        verify(child).println(eq(99), isNull(), eq("HelloWorldMsg"), isNull());
    }

    @Test
    public void testNoNextNodeIsSafePublic() {
        MessageOnlyLogFilter filter = new MessageOnlyLogFilter();
        // Should not throw
        filter.println(88, "AnotherTAG", "SomeMessage", null);
        // Nothing to verify, just confirms no exception
    }

    @Test
    public void testChainedNextNodePublic() {
        MessageOnlyLogFilter filter = new MessageOnlyLogFilter();
        LogNode chainChild = mock(LogNode.class, "publicChainChild");
        filter.setNext(chainChild);

        filter.println(5, "TagChain", "ChainedMsg", new RuntimeException("publicChain"));
        verify(chainChild).println(eq(5), isNull(), eq("ChainedMsg"), isNull());
    }
}