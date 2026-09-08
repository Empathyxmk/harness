package com.example.android.common.logger;

import org.junit.*;

import static org.mockito.Mockito.*;

public class LogTest {

    LogNode mockNode;

    @Before
    public void setUp() {
        mockNode = mock(LogNode.class);
        Log.setLogNode(mockNode);
    }

    @After
    public void tearDown() {
        Log.setLogNode(null);
    }

    @Test
    public void testSetAndGetLogNode() {
        Assert.assertEquals(mockNode, Log.getLogNode());
    }

    @Test
    public void testPrintlnCallsNode() {
        Log.println(Log.DEBUG, "TAG", "msg", null);
        verify(mockNode).println(Log.DEBUG, "TAG", "msg", null);

        Log.println(Log.INFO, "TAG2", "msg2");
        verify(mockNode).println(Log.INFO, "TAG2", "msg2", null);
    }

    @Test
    public void testVerbosityDelegates() {
        Log.v("V", "verbose");
        verify(mockNode).println(eq(Log.VERBOSE), eq("V"), eq("verbose"), isNull());

        Log.v("V2", "verbose2", new RuntimeException("err"));
        verify(mockNode).println(eq(Log.VERBOSE), eq("V2"), eq("verbose2"), any());
    }

    @Test
    public void testDebugDelegates() {
        Log.d("D", "debug");
        verify(mockNode).println(eq(Log.DEBUG), eq("D"), eq("debug"), isNull());

        Log.d("D2", "debug2", new Exception("err"));
        verify(mockNode).println(eq(Log.DEBUG), eq("D2"), eq("debug2"), any());
    }

    @Test
    public void testInfoDelegates() {
        Log.i("I", "info");
        verify(mockNode).println(eq(Log.INFO), eq("I"), eq("info"), isNull());

        Log.i("I2", "info2", new Exception("err"));
        verify(mockNode).println(eq(Log.INFO), eq("I2"), eq("info2"), any());
    }

    @Test
    public void testWarnDelegates() {
        Log.w("W", "warn");
        verify(mockNode).println(eq(Log.WARN), eq("W"), eq("warn"), isNull());

        Log.w("W2", "warn2", new Exception("err"));
        verify(mockNode).println(eq(Log.WARN), eq("W2"), eq("warn2"), any());
    }

    @Test
    public void testErrorDelegates() {
        Log.e("E", "error");
        verify(mockNode).println(eq(Log.ERROR), eq("E"), eq("error"), isNull());

        Log.e("E2", "error2", new Exception("err"));
        verify(mockNode).println(eq(Log.ERROR), eq("E2"), eq("error2"), any());
    }

    @Test
    public void testWtfDelegates() {
        Log.wtf("T", "assert");
        verify(mockNode).println(eq(Log.ASSERT), eq("T"), eq("assert"), isNull());

        Log.wtf("T2", "assert2", new Exception("err"));
        verify(mockNode).println(eq(Log.ASSERT), eq("T2"), eq("assert2"), any());
    }

    @Test
    public void testNoNodeDoesNotCrash() {
        Log.setLogNode(null);
        // Should not throw
        Log.d("TAG", "Should do nothing");
    }
}