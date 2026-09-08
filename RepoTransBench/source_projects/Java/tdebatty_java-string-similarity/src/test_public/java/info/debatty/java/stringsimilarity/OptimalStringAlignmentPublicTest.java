package info.debatty.java.stringsimilarity;

import org.junit.Test;
import static org.junit.Assert.assertEquals;

public class OptimalStringAlignmentPublicTest {

    @Test
    public void testDistance() {
        OptimalStringAlignment osa = new OptimalStringAlignment();
        assertEquals(2.0, osa.distance("cats", "acts"), 0.001); // transposition + substitution
        assertEquals(3.0, osa.distance("algorithm", "algorihtm"), 0.001); // two transpositions
        assertEquals(1.0, osa.distance("listing", "listers"), 0.001);
    }

    @Test
    public void testDistanceWithLimit() {
        OptimalStringAlignment osa = new OptimalStringAlignment();
        assertEquals(1.0, osa.distance("bake", "cake", 2), 0.001);
        assertEquals(2.0, osa.distance("bike", "cake", 1), 0.001);
        assertEquals(3.0, osa.distance("park", "track", 2), 0.001);
        assertEquals(2.0, osa.distance("suite", "quite", 1), 0.001);
    }
}