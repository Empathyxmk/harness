package edu.cmu.pocketsphinx;

import org.junit.Test;

import static org.junit.Assert.*;

public class HypothesisPublicTest {

    @Test
    public void testGettersWithDifferentValues() {
        Hypothesis h = new Hypothesis("public test string", 123);
        assertEquals("public test string", h.getHypstr());
        assertEquals(123, h.getBestScore());
    }

    @Test
    public void testWhitespaceText() {
        Hypothesis h = new Hypothesis("    ", 1000);
        assertEquals("    ", h.getHypstr());
        assertEquals(1000, h.getBestScore());
    }

    @Test
    public void testLargeNegativeScore() {
        Hypothesis h = new Hypothesis("edge", -999999);
        assertEquals("edge", h.getHypstr());
        assertEquals(-999999, h.getBestScore());
    }
}