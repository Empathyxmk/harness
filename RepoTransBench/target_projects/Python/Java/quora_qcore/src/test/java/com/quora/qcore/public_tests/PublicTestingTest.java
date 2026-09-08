package com.quora.qcore.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicTestingTest {
    @Test
    public void testDummyObjectAttrs() {
        DummyObject x = new DummyObject(2, "foo", null);
        assertEquals(2, x.getA());
        assertEquals("foo", x.getB());
    }
    static class DummyObject {
        private final int a; private final String b; private final Object c;
        public DummyObject(int a, String b, Object c) { this.a=a; this.b=b; this.c=c;}
        public int getA() { return a; }
        public String getB() { return b; }
        public Object getC() { return c; }
    }
}