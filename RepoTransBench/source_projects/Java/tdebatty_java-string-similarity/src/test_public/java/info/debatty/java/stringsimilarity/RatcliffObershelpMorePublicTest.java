package info.debatty.java.stringsimilarity;

import org.junit.Test;
import static org.junit.Assert.*;

public class RatcliffObershelpMorePublicTest {
    RatcliffObershelp ro = new RatcliffObershelp();

    @Test(expected = NullPointerException.class)
    public void testSimilarityNullFirst() {
        ro.similarity(null, "xyz");
    }

    @Test(expected = NullPointerException.class)
    public void testSimilarityNullSecond() {
        ro.similarity("xyz", null);
    }

    @Test
    public void testDistanceProperty() {
        assertEquals(0.0, ro.distance("banana", "banana"), 1e-9);
        assertTrue(ro.distance("basket", "apple") > 0.8);
    }

    @Test
    public void testEmptyStrings() {
        assertEquals(1.0, ro.similarity("", ""), 1e-9);
        assertEquals(0.0, ro.similarity("", "banana"), 1e-9);
        assertEquals(0.0, ro.similarity("banana", ""), 1e-9);
    }

    @Test
    public void testPartialMatching() {
        assertTrue(ro.similarity("testing", "resting") < 1.0);
        assertTrue(ro.similarity("cat", "dog") < 1.0);
    }
}