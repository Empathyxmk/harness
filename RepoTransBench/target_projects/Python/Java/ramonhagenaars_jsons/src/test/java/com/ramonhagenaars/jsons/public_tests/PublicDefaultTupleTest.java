package com.ramonhagenaars.jsons.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicDefaultTupleTest {

    @Test
    void testDefaultTupleDumpPublic() {
        Pair<Integer, String> pair = new Pair<>(42, "answer");
        assertEquals(42, pair.first.intValue());
        assertEquals("answer", pair.second);
        assertEquals("Pair{first=42, second=answer}", pair.toString());
    }

    @Test
    void testDefaultTupleLoadPublic() {
        Pair<Double, Integer> pair = Pair.fromString("3.14:7");
        assertEquals(3.14, pair.first, 1e-10);
        assertEquals(7, pair.second.intValue());
    }

    static class Pair<A, B> {
        final A first;
        final B second;

        Pair(A first, B second) {
            this.first = first;
            this.second = second;
        }
        static Pair<Double, Integer> fromString(String s) {
            String[] parts = s.split(":");
            return new Pair<>(Double.valueOf(parts[0]), Integer.valueOf(parts[1]));
        }
        @Override
        public String toString() {
            return "Pair{first=" + first + ", second=" + second + "}";
        }
        @Override
        public boolean equals(Object o) {
            if (!(o instanceof Pair)) return false;
            Pair<?, ?> p = (Pair<?, ?>) o;
            return first.equals(p.first) && second.equals(p.second);
        }
        @Override
        public int hashCode() {
            return first.hashCode() * 31 + second.hashCode();
        }
    }
}