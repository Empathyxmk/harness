package com.trailofbits.protofuzz.public_tests;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

import java.util.Iterator;
import java.util.ArrayList;
import java.util.List;

public class PublicProtofuzzTest {
    static class SimpleNamespace {
        public int y;
    }

    interface GenFunc<T> {
        Iterator<T> generator();
    }

    public static GenFunc<SimpleNamespace> messageStrategy() {
        return () -> new Iterator<SimpleNamespace>() {
            boolean yielded = false;
            @Override
            public boolean hasNext() { return !yielded; }

            @Override
            public SimpleNamespace next() {
                if (!yielded) {
                    SimpleNamespace msg = new SimpleNamespace();
                    msg.y = 42;
                    yielded = true;
                    return msg;
                }
                throw new java.util.NoSuchElementException();
            }
        };
    }

    @Test
    public void testMessageStrategyPublic() {
        GenFunc<SimpleNamespace> strat = messageStrategy();
        Iterator<SimpleNamespace> g = strat.generator();
        SimpleNamespace msg = g.next();
        assertNotNull(msg);
        assertTrue(msg instanceof SimpleNamespace);
        assertEquals(42, msg.y);
    }

    @Test
    public void testFuzzPublic() {
        Iterator<String> strat = new Iterator<String>() {
            private int state = 0;
            @Override
            public boolean hasNext() { return state < 3; }
            @Override
            public String next() {
                switch (state++) {
                    case 0: return "D";
                    case 1: return "E";
                    case 2: return "F";
                    default: throw new java.util.NoSuchElementException();
                }
            }
        };
        List<String> results = new ArrayList<>();
        int count = 0;
        while (strat.hasNext() && count < 3) {
            results.add(strat.next());
            count++;
        }
        assertEquals(java.util.Arrays.asList("D", "E", "F"), results);
    }
}