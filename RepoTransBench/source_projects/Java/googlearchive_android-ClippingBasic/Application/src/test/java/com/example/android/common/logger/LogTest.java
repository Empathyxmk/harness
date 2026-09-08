package com.example.android.common.logger;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class LogTest {

    static class TestLogNode implements LogNode {
        public int priority;
        public String tag;
        public String msg;
        public Throwable tr;

        @Override
        public void println(int priority, String tag, String msg, Throwable tr) {
            this.priority = priority;
            this.tag = tag;
            this.msg = msg;
            this.tr = tr;
        }
    }

    private TestLogNode testNode;

    @Before
    public void setUp() {
        testNode = new TestLogNode();
        Log.setLogNode(testNode);
    }

    @Test
    public void testSetAndGetLogNode() {
        Log.setLogNode(testNode);
        assertEquals(testNode, Log.getLogNode());
    }

    @Test
    public void testPrintlnWithThrowable() {
        Throwable tr = new RuntimeException("Exception");
        Log.println(Log.DEBUG, "TAG", "msg", tr);
        assertEquals(Log.DEBUG, testNode.priority);
        assertEquals("TAG", testNode.tag);
        assertEquals("msg", testNode.msg);
        assertEquals(tr, testNode.tr);
    }

    @Test
    public void testPrintlnWithoutThrowable() {
        Log.println(Log.INFO, "TAG2", "msg2");
        assertEquals(Log.INFO, testNode.priority);
        assertEquals("TAG2", testNode.tag);
        assertEquals("msg2", testNode.msg);
        assertNull(testNode.tr);
    }

    @Test
    public void testLevelShortcuts() {
        Log.v("TAGv", "verbose");
        assertEquals(Log.VERBOSE, testNode.priority);
        Log.d("TAGd", "debug");
        assertEquals(Log.DEBUG, testNode.priority);
        Log.i("TAGi", "info");
        assertEquals(Log.INFO, testNode.priority);
        Log.w("TAGw", "warn");
        assertEquals(Log.WARN, testNode.priority);
        Log.e("TAGe", "error", new NullPointerException());
        assertEquals(Log.ERROR, testNode.priority);
        Log.wtf("TAGa", "assert");
        assertEquals(Log.ASSERT, testNode.priority);
    }

    @Test
    public void testNoLogNodeSet() {
        Log.setLogNode(null);
        // Should not throw even if node is null
        Log.println(Log.DEBUG, "TAG", "msg", null);
    }
}