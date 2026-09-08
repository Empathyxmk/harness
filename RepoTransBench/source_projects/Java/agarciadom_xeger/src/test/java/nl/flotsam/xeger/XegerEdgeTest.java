package nl.flotsam.xeger;

import org.junit.Test;

import java.util.Random;

import static org.junit.Assert.*;

public class XegerEdgeTest {

    @Test(expected = IllegalArgumentException.class)
    public void testInvalidRegexThrowsException() {
        // Unclosed bracket
        new Xeger("[A-Z", new Random());
    }

    @Test
    public void testGenerateMinEqualsMax() throws Exception {
        Xeger generator = new Xeger("[ab]{3,3}c", new Random(42));
        String s = generator.generate(4, 4);
        assertEquals(4, s.length());
        assertTrue(s.matches("[ab]{3}c"));
    }

    @Test(expected = Xeger.FailedRandomWalkException.class)
    public void testGenerateTooShortThrowsException() throws Exception {
        Xeger generator = new Xeger("abc", new Random(42));
        // ask for longer than regex allows to force fail
        generator.generate(4, 4);
    }

    @Test
    public void testGenerateAcceptOnFirstStep() throws Exception {
        // Regex that can accept on empty string
        Xeger generator = new Xeger("a*", new Random(42));
        String s = generator.generate(0, 0);
        assertTrue(s.matches("a*"));
        assertEquals(0, s.length());
    }

    @Test
    public void testGenerateNormalFlow() throws Exception {
        Xeger generator = new Xeger("abc|def", new Random(1));
        String s = generator.generate();
        assertTrue(s.equals("abc") || s.equals("def"));
    }
}