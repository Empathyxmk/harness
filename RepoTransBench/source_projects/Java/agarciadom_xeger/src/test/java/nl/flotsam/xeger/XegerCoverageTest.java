package nl.flotsam.xeger;

import static org.junit.Assert.*;
import org.junit.Test;

import java.util.Random;

public class XegerCoverageTest {

    @Test
    public void testConstructorWithRandom() {
        Xeger xeger = new Xeger("abc|def", new Random(123));
        assertNotNull(xeger);
        assertNotNull(xeger.getRandom());
    }

    @Test
    public void testSetAndGetRandom() {
        Xeger xeger = new Xeger("a+", new Random(123));
        Random r = new Random(456);
        xeger.setRandom(r);
        assertSame(r, xeger.getRandom());
    }

    @Test
    public void testGenerateSimpleLiteral() {
        Xeger xeger = new Xeger("abc", new Random(321));
        String generated = xeger.generate();
        assertEquals("abc", generated);
    }

    @Test
    public void testGenerateWithDefaultRandom() {
        // Covers the constructor Xeger(String) that creates Random internally.
        Xeger xeger = new Xeger("b");
        String generated = xeger.generate();
        assertEquals("b", generated);
    }

    @Test
    public void testGetRandomIntWorksOnSimpleCases() {
        int result = Xeger.getRandomInt(5, 5, new Random(1));
        assertEquals(5, result);

        int result2 = Xeger.getRandomInt(1, 10, new Random(1));
        assertTrue(1 <= result2 && result2 <= 10);
    }

    @Test
    public void testGenerateWithBoundedLengthThrowsMinimum() {
        Xeger xeger = new Xeger("a?", new Random(1));
        try {
            xeger.generate(2, 2);
            fail("Should have thrown FailedRandomWalkException");
        } catch (Xeger.FailedRandomWalkException ex) {
            // Accept both possible messages, for robust assertion
            assertTrue(
                ex.getMessage().contains("current = 0 < min = 2")
                || ex.getMessage().contains("current = 1 < min = 2")
            );
        }
    }

    @Test
    public void testGenerateWithBoundedLengthThrowsMaximum() {
        Xeger xeger = new Xeger("a{3}", new Random(1));
        try {
            xeger.generate(1, 2); // regex "a{3}" requires at least 3 chars, max is lower
            fail("Should have thrown FailedRandomWalkException");
        } catch (Xeger.FailedRandomWalkException ex) {
            assertTrue(ex.getMessage().toLowerCase().contains("exceeded maximum walk length"));
        }
    }

    @Test
    public void testGenerateWithBoundedLengthProducesAcceptableLength() throws Exception {
        Xeger xeger = new Xeger("a{2,4}", new Random(2));
        String val = xeger.generate(2, 4);
        assertTrue(val.matches("a{2,4}"));
        assertTrue(val.length() >= 2 && val.length() <= 4);
    }

    @Test
    public void testFailedRandomWalkException() {
        Xeger.FailedRandomWalkException ex = new Xeger.FailedRandomWalkException("fail");
        assertNotNull(ex.getMessage());
        assertEquals("fail", ex.getMessage());
    }

    @Test
    public void testAppendRandomChoiceMinLength() throws Exception {
        // Indirect coverage via generate(), but call directly
        Xeger xeger = new Xeger("ab?", new Random(3));
        java.lang.reflect.Method method = Xeger.class.getDeclaredMethod("appendRandomChoice", StringBuilder.class, Class.forName("dk.brics.automaton.State"), int.class, int.class);
        method.setAccessible(true);
        // setup for state
        dk.brics.automaton.State st = new dk.brics.automaton.RegExp("a?b").toAutomaton().getInitialState();
        Object result = method.invoke(xeger, new StringBuilder(), st, 0, 0);
        assertNotNull(result); // should return Optional
    }
}