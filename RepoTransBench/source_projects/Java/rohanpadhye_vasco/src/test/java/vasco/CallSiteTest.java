package vasco;

import static org.junit.Assert.*;
import org.junit.Test;

public class CallSiteTest {

    static class DummyContext extends Context<String, String, Integer> {
        private final int id;

        public DummyContext(int id) {
            super("m", null, false);
            this.id = id;
        }

        @Override
        public int getId() {
            return id;
        }

        @Override
        public boolean equals(Object obj) {
            if (!(obj instanceof DummyContext)) return false;
            return this.id == ((DummyContext) obj).id;
        }

        @Override
        public int hashCode() {
            return id;
        }
    }

    @Test
    public void testEqualsAndHashCode() {
        DummyContext ctx1 = new DummyContext(1);
        DummyContext ctx2 = new DummyContext(2);
        CallSite<String, String, Integer> cs1 = new CallSite<>(ctx1, "call1");
        CallSite<String, String, Integer> cs2 = new CallSite<>(ctx1, "call1");
        CallSite<String, String, Integer> cs3 = new CallSite<>(ctx1, "call2");
        CallSite<String, String, Integer> cs4 = new CallSite<>(ctx2, "call1");

        assertTrue(cs1.equals(cs2));
        assertEquals(cs1.hashCode(), cs2.hashCode());

        assertFalse(cs1.equals(cs3));
        assertFalse(cs1.equals(cs4));
        assertFalse(cs1.equals(null));
        assertFalse(cs1.equals("SomeString"));
    }

    @Test
    public void testCompareTo() {
        DummyContext ctx1 = new DummyContext(1);
        DummyContext ctx2 = new DummyContext(4);
        CallSite<String, String, Integer> cs1 = new CallSite<>(ctx1, "c1");
        CallSite<String, String, Integer> cs2 = new CallSite<>(ctx2, "c1");

        assertTrue(cs1.compareTo(cs2) < 0);
        assertTrue(cs2.compareTo(cs1) > 0);
        assertEquals(0, cs1.compareTo(new CallSite<>(ctx1, "c2")));
    }

    @Test
    public void testGettersToString() {
        DummyContext ctx1 = new DummyContext(42);
        CallSite<String, String, Integer> cs1 = new CallSite<>(ctx1, "stmtNode");
        assertEquals(ctx1, cs1.getCallingContext());
        assertEquals("stmtNode", cs1.getCallNode());
        assertTrue(cs1.toString().contains("42"));
        assertTrue(cs1.toString().contains("stmtNode"));
    }
}