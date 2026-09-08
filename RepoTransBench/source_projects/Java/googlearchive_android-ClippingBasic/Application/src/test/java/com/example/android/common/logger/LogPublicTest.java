package com.example.android.common.logger;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class LogPublicTest {

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
    public void testSetAndGetLogNodePublic() {
        Log.setLogNode(testNode);
        assertEquals(testNode, Log.getLogNode());
    }

    @Test
    public void testPrintlnWithThrowablePublic() {
        Throwable tr = new IllegalArgumentException("PublicException");
        Log.println(Log.ERROR, "PUB", "public_msg", tr);
        assertEquals(Log.ERROR, testNode.priority);
        assertEquals("PUB", testNode.tag);
        assertEquals("public_msg", testNode.msg);
        assertEquals(tr, testNode.tr);
    }

    @Test
    public void testPrintlnWithoutThrowablePublic() {
        Log.println(Log.WARN, "PUB2", "public_msg2");
        assertEquals(Log.WARN, testNode.priority);
        assertEquals("PUB2", testNode.tag);
        assertEquals("public_msg2", testNode.msg);
        assertNull(testNode.tr);
    }

    @Test
    public void testLevelShortcutsPublic() {
        Log.v("PUBv", "visible");
        assertEquals(Log.VERBOSE, testNode.priority);
        Log.d("PUBd", "debugging");
        assertEquals(Log.DEBUG, testNode.priority);
        Log.i("PUBi", "information");
        assertEquals(Log.INFO, testNode.priority);
        Log.w("PUBw", "warning");
        assertEquals(Log.WARN, testNode.priority);
        Log.e("PUBe", "error occurred", new IllegalStateException());
        assertEquals(Log.ERROR, testNode.priority);
        Log.wtf("PUBa", "assertion");
        assertEquals(Log.ASSERT, testNode.priority);
    }

    @Test
    public void testNoLogNodeSetPublic() {
        Log.setLogNode(null);
        // Should not throw even if node is null
        Log.println(Log.INFO, "PUB", "public_msg", null);
    }
}