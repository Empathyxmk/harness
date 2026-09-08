package com.example.android.common.logger;

import org.junit.*;
import static org.mockito.Mockito.*;

public class LogPublicTest {

    LogNode mockNode;

    @Before
    public void setUp() {
        mockNode = mock(LogNode.class, "publicMockNode");
        Log.setLogNode(mockNode);
    }

    @After
    public void tearDown() {
        Log.setLogNode(null);
    }

    @Test
    public void testSetAndGetLogNodePublic() {
        Assert.assertSame(mockNode, Log.getLogNode());
    }

    @Test
    public void testPrintlnCallsNodeWithDifferentValues() {
        Log.println(Log.INFO, "PUB_TAG", "publicMsg", null);
        verify(mockNode).println(Log.INFO, "PUB_TAG", "publicMsg", null);

        Log.println(Log.WARN, "PUB_TAG_WARN", "warnMsg");
        verify(mockNode).println(Log.WARN, "PUB_TAG_WARN", "warnMsg", null);
    }

    @Test
    public void testVerboseDelegatesWithDifferentInput() {
        Log.v("VerboseTag", "verbMsg");
        verify(mockNode).println(eq(Log.VERBOSE), eq("VerboseTag"), eq("verbMsg"), isNull());

        Log.v("VerbTag2", "verbMsg2", new IllegalArgumentException("public"));
        verify(mockNode).println(eq(Log.VERBOSE), eq("VerbTag2"), eq("verbMsg2"), any());
    }

    @Test
    public void testDebugDelegatesWithDifferentInput() {
        Log.d("DebugTag", "debugMessage");
        verify(mockNode).println(eq(Log.DEBUG), eq("DebugTag"), eq("debugMessage"), isNull());

        Log.d("DebugTag2", "debugMessage2", new IllegalStateException("failure"));
        verify(mockNode).println(eq(Log.DEBUG), eq("DebugTag2"), eq("debugMessage2"), any());
    }

    @Test
    public void testInfoDelegatesWithPublicData() {
        Log.i("InfoTag", "infoMsg1");
        verify(mockNode).println(eq(Log.INFO), eq("InfoTag"), eq("infoMsg1"), isNull());

        Log.i("InfoTag2", "infoMsg2", new NullPointerException("infoNull"));
        verify(mockNode).println(eq(Log.INFO), eq("InfoTag2"), eq("infoMsg2"), any());
    }

    @Test
    public void testWarnDelegatesPublic() {
        Log.w("WarnTag", "warnMsg1");
        verify(mockNode).println(eq(Log.WARN), eq("WarnTag"), eq("warnMsg1"), isNull());

        Log.w("WarnTag2", "warnMsg2", new ArithmeticException("warnArith"));
        verify(mockNode).println(eq(Log.WARN), eq("WarnTag2"), eq("warnMsg2"), any());
    }

    @Test
    public void testErrorDelegatesPublic() {
        Log.e("ErrorTag", "errorMsg1");
        verify(mockNode).println(eq(Log.ERROR), eq("ErrorTag"), eq("errorMsg1"), isNull());

        Log.e("ErrorTag2", "errorMsg2", new RuntimeException("publicError"));
        verify(mockNode).println(eq(Log.ERROR), eq("ErrorTag2"), eq("errorMsg2"), any());
    }

    @Test
    public void testWtfDelegatesWithDifferentData() {
        Log.wtf("AssertT", "assertMsg");
        verify(mockNode).println(eq(Log.ASSERT), eq("AssertT"), eq("assertMsg"), isNull());

        Log.wtf("AssertT2", "assertMsg2", new Throwable("assertThrowable"));
        verify(mockNode).println(eq(Log.ASSERT), eq("AssertT2"), eq("assertMsg2"), any());
    }

    @Test
    public void testNoNodeSafeOnNullPublic() {
        Log.setLogNode(null);
        // Should not throw an exception
        Log.i("SafeTAG", "ShouldBeSafe");
    }
}