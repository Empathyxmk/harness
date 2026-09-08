package com.vijos.jd4.public_tests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class PublicCaseTest {

    static class Case implements Comparable<Case> {
        private final String name, input, output;
        private final int score;

        public Case(String name, String input, String output, int score) {
            this.name = name;
            this.input = input;
            this.output = output;
            this.score = score;
        }

        public String getName() { return name; }
        public String getInput() { return input; }
        public String getOutput() { return output; }
        public int getScore() { return score; }

        @Override public String toString() {
            return name + ":" + input + "/" + output + " score=" + score;
        }
        @Override public String toString() { return toString(); }
        @Override public String toString() { return toString(); }
        @Override public boolean equals(Object o) {
            if (!(o instanceof Case)) return false;
            Case c = (Case) o;
            return name.equals(c.name) && input.equals(c.input) && output.equals(c.output) && score == c.score;
        }
        @Override public int compareTo(Case o) {
            return name.compareTo(o.name);
        }
    }

    @Test
    void testCaseReprDiffParams() {
        Case c = new Case("test_case2", "input-42", "output-99", 15);
        String r = c.toString();
        assertTrue(r.contains("test_case2"));
        assertTrue(r.contains("score=15"));
    }

    @Test
    void testCasePropertiesDifferent() {
        Case c = new Case("sampleB", "abc", "def", 8);
        assertEquals("sampleB", c.getName());
        assertEquals("abc", c.getInput());
        assertEquals("def", c.getOutput());
        assertEquals(8, c.getScore());
    }

    @Test
    void testCaseEqFalse() {
        Case c = new Case("eqtest2", "in", "out", 1);
        assertNotEquals(c, Integer.valueOf(42));
        assertFalse(c.equals(42));
    }

    @Test
    void testCaseOrderingDifferentName() {
        Case c1 = new Case("case0002", "", "", 0);
        Case c2 = new Case("case0010", "", "", 0);
        assertTrue(c1.compareTo(c2) < 0);
    }

    @Test
    void testCaseStrContent() {
        Case c = new Case("visible2", "inputY", "outputY", 4);
        String s = c.toString();
        assertTrue(s.contains("visible2"));
        assertTrue(s.contains("inputY"));
        assertTrue(s.contains("outputY"));
        assertTrue(s.contains("score=4"));
    }
}