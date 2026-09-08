package info.debatty.java.stringsimilarity;

import org.junit.Test;
import static org.junit.Assert.assertEquals;

public class LevenshteinPublicTest {

    @Test
    public final void testDistance() {
        System.out.println("public distance");
        Levenshtein instance = new Levenshtein();
        assertEquals(2.0, instance.distance("hello", "hallo"), 0.0);
        assertEquals(3.0, instance.distance("goodbye", "badbye!"), 0.0);
        assertEquals(1.0, instance.distance("help", "yelp"), 0.0);

        // With limits.
        assertEquals(2.0, instance.distance("goodbye", "badbye!", 4), 0.0);
        assertEquals(3.0, instance.distance("goodbye", "badbye!", 2), 0.0);
        assertEquals(2.0, instance.distance("goodbye", "badbye!", 1), 0.0);
    }
}