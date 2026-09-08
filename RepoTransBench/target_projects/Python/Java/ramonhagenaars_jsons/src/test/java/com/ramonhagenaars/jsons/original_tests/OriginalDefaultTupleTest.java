package com.ramonhagenaars.jsons.original_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class OriginalDefaultTupleTest {

    static class MyTuple<A, B, C> {
        final A first;
        final B second;
        final C third;
        MyTuple(A first, B second, C third) {
            this.first = first;
            this.second = second;
            this.third = third;
        }
        @Override
        public boolean equals(Object o) {
            if (!(o instanceof MyTuple)) return false;
            MyTuple<?,?,?> t = (MyTuple<?,?,?>) o;
            return first.equals(t.first) && second.equals(t.second) && third.equals(t.third);
        }
        @Override
        public int hashCode() {
            return first.hashCode() + second.hashCode() + third.hashCode();
        }
    }

    @Test
    void testTupleCreate() {
        MyTuple<Integer, String, Double> t = new MyTuple<>(7, "foo", 6.7);
        assertEquals(7, t.first.intValue());
        assertEquals("foo", t.second);
        assertEquals(6.7, t.third, 1e-9);
    }

    @Test
    void testTupleEquals() {
        MyTuple<String, String, String> t1 = new MyTuple<>("a", "b", "c");
        MyTuple<String, String, String> t2 = new MyTuple<>("a", "b", "c");
        assertEquals(t1, t2);
    }
}