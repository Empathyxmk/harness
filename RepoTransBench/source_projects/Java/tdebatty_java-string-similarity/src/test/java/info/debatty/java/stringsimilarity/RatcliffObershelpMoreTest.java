package info.debatty.java.stringsimilarity;

import org.junit.Test;
import static org.junit.Assert.*;

public class RatcliffObershelpMoreTest {
    RatcliffObershelp ro = new RatcliffObershelp();

    @Test(expected = NullPointerException.class)
    public void testSimilarityNullFirst() {
        ro.similarity(null, "abc");
    }

    @Test(expected = NullPointerException.class)
    public void testSimilarityNullSecond() {
        ro.similarity("abc", null);
    }

    @Test
    public void testDistanceProperty() {
        assertEquals(0.0, ro.distance("abc", "abc"), 1e-9);
        assertTrue(ro.distance("abcd", "xyz") > 0.9);
    }

    @Test
    public void testEmptyStrings() {
        assertEquals(1.0, ro.similarity("", ""), 1e-9);
        assertEquals(0.0, ro.similarity("", "abc"), 1e-9);
        assertEquals(0.0, ro.similarity("abc", ""), 1e-9);
    }

    @Test
    public void testPartialMatching() {
        assertTrue(ro.similarity("hello", "yellow") < 1.0);
        assertTrue(ro.similarity("foo", "bar") < 1.0);
    }
}