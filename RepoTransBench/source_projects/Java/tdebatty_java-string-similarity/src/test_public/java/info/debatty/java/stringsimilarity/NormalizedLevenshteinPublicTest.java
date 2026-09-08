package info.debatty.java.stringsimilarity;

import org.junit.Test;
import static org.junit.Assert.*;

public class NormalizedLevenshteinPublicTest {

    @Test
    public void testDistance() {
        NormalizedLevenshtein nl = new NormalizedLevenshtein();
        assertEquals(2.0/4.0, nl.distance("ABCD", "ACFD"), 0.0001);
        assertEquals(1.0/6.0, nl.distance("banana", "banaba"), 0.0001);
        assertEquals(3.0/7.0, nl.distance("compete", "compute"), 0.0001);
    }

    @Test
    public void testSimilarity() {
        NormalizedLevenshtein nl = new NormalizedLevenshtein();
        assertEquals(1.0 - 2.0/4.0, nl.similarity("ABCD", "ACFD"), 0.0001);
        assertEquals(5.0/6.0, nl.similarity("banana", "banaba"), 0.0001);
        assertEquals(4.0/7.0, nl.similarity("compete", "compute"), 0.0001);
    }

    @Test
    public void testEmpty() {
        NormalizedLevenshtein nl = new NormalizedLevenshtein();
        assertEquals(1.0, nl.similarity("", ""), 1e-9);
        assertEquals(0.0, nl.similarity("", "test"), 1e-9);
        assertEquals(0.0, nl.similarity("test", ""), 1e-9);
    }
}