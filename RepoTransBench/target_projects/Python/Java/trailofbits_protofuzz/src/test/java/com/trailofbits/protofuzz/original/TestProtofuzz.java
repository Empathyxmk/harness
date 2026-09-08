package com.trailofbits.protofuzz.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

import java.util.Iterator;

// Simulate protofuzz.message_strategy and protofuzz.fuzz with static helper methods
public class TestProtofuzz {

    static class SimpleNamespace {
        // dynamic properties
        public int x;
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
                    msg.x = 1;
                    yielded = true;
                    return msg;
                }
                throw new java.util.NoSuchElementException();
            }
        };
    }

    @Test
    public void testMessageStrategySmoke() {
        GenFunc<SimpleNamespace> strat = messageStrategy();
        Iterator<SimpleNamespace> g = strat.generator();
        SimpleNamespace msg = g.next();
        assertNotNull(msg);
        assertEquals(1, msg.x);
    }

    @Test
    public void testFuzzSmoke() {
        // Generator yields "A", "B", "C"
        Iterator<String> strat = new Iterator<String>() {
            private int state = 0;
            @Override
            public boolean hasNext() { return state < 3; }
            @Override
            public String next() {
                switch (state++) {
                    case 0: return "A";
                    case 1: return "B";
                    case 2: return "C";
                    default: throw new java.util.NoSuchElementException();
                }
            }
        };
        java.util.List<String> results = new java.util.ArrayList<>();
        // Simulate fuzz logic (just pull at most 3 values)
        int count = 0;
        while (strat.hasNext() && count < 3) {
            results.add(strat.next());
            count++;
        }
        assertEquals(java.util.Arrays.asList("A", "B", "C"), results);
    }
}