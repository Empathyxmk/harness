package nl.flotsam.xeger;

import org.junit.Test;

import java.util.Random;

import static org.junit.Assert.*;

public class XegerEdgePublicTest {

    @Test(expected = IllegalArgumentException.class)
    public void testInvalidRegexThrowsException() {
        // Unclosed parenthesis instead (different from bracket)
        new Xeger("(abc", new Random());
    }

    @Test
    public void testGenerateMinEqualsMax() throws Exception {
        Xeger generator = new Xeger("[cd]{2,2}e", new Random(77));
        String s = generator.generate(3, 3);
        assertEquals(3, s.length());
        assertTrue(s.matches("[cd]{2}e"));
    }

    @Test(expected = Xeger.FailedRandomWalkException.class)
    public void testGenerateTooShortThrowsException() throws Exception {
        Xeger generator = new Xeger("xyz", new Random(13));
        // ask for more than available length to force fail
        generator.generate(5, 5);
    }

    @Test
    public void testGenerateAcceptOnFirstStep() throws Exception {
        // Regex that can accept empty string, test min-length 0 as before
        Xeger generator = new Xeger("b*", new Random(11));
        String s = generator.generate(0, 0);
        assertTrue(s.matches("b*"));
        assertEquals(0, s.length());
    }

    @Test
    public void testGenerateNormalFlow() throws Exception {
        Xeger generator = new Xeger("abc|xyz", new Random(3));
        String s = generator.generate();
        assertTrue(s.equals("abc") || s.equals("xyz"));
    }
}