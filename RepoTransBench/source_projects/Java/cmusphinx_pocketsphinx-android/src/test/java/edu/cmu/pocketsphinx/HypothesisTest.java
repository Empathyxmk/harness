package edu.cmu.pocketsphinx;

import org.junit.Test;

import static org.junit.Assert.*;

public class HypothesisTest {

    @Test
    public void testGetters() {
        Hypothesis h = new Hypothesis("hello world", 42);
        assertEquals("hello world", h.getHypstr());
        assertEquals(42, h.getBestScore());
    }

    @Test
    public void testEmptyText() {
        Hypothesis h = new Hypothesis("", 0);
        assertEquals("", h.getHypstr());
        assertEquals(0, h.getBestScore());
    }

    @Test
    public void testNegativeScore() {
        Hypothesis h = new Hypothesis("neg", -1);
        assertEquals("neg", h.getHypstr());
        assertEquals(-1, h.getBestScore());
    }
}