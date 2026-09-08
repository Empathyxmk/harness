package nl.flotsam.xeger;

import static org.junit.Assert.*;
import org.junit.Test;

import java.util.Random;

public class XegerCoveragePublicTest {

    @Test
    public void testConstructorWithRandom() {
        Xeger xeger = new Xeger("xyz|uvw", new Random(321));
        assertNotNull(xeger);
        assertNotNull(xeger.getRandom());
    }

    @Test
    public void testSetAndGetRandom() {
        Xeger xeger = new Xeger("b+", new Random(4545));
        Random r = new Random(999);
        xeger.setRandom(r);
        assertSame(r, xeger.getRandom());
    }

    @Test
    public void testGenerateSimpleLiteral() {
        Xeger xeger = new Xeger("acd", new Random(222));
        String generated = xeger.generate();
        assertEquals("acd", generated);
    }

    @Test
    public void testGenerateWithDefaultRandom() {
        Xeger xeger = new Xeger("z");
        String generated = xeger.generate();
        assertEquals("z", generated);
    }

    @Test
    public void testGetRandomIntWorksOnSimpleCases() {
        int result = Xeger.getRandomInt(8, 8, new Random(5));
        assertEquals(8, result);

        int result2 = Xeger.getRandomInt(2, 8, new Random(7));
        assertTrue(2 <= result2 && result2 <= 8);
    }

    @Test
    public void testGenerateWithBoundedLengthThrowsMinimum() {
        Xeger xeger = new Xeger("b?", new Random(4));
        try {
            xeger.generate(2, 2);
            fail("Should have thrown FailedRandomWalkException");
        } catch (Xeger.FailedRandomWalkException ex) {
            assertTrue(
                ex.getMessage().contains("current = 0 < min = 2")
                || ex.getMessage().contains("current = 1 < min = 2")
            );
        }
    }

    @Test
    public void testGenerateWithBoundedLengthThrowsMaximum() {
        Xeger xeger = new Xeger("b{5}", new Random(4));
        try {
            xeger.generate(1, 3); // regex "b{5}" requires at least 5 chars, max is lower
            fail("Should have thrown FailedRandomWalkException");
        } catch (Xeger.FailedRandomWalkException ex) {
            assertTrue(ex.getMessage().toLowerCase().contains("exceeded maximum walk length"));
        }
    }

    @Test
    public void testGenerateWithBoundedLengthProducesAcceptableLength() throws Exception {
        Xeger xeger = new Xeger("c{1,3}", new Random(5));
        String val = xeger.generate(1, 3);
        assertTrue(val.matches("c{1,3}"));
        assertTrue(val.length() >= 1 && val.length() <= 3);
    }

    @Test
    public void testFailedRandomWalkException() {
        Xeger.FailedRandomWalkException ex = new Xeger.FailedRandomWalkException("another fail");
        assertNotNull(ex.getMessage());
        assertEquals("another fail", ex.getMessage());
    }

    @Test
    public void testAppendRandomChoiceMinLength() throws Exception {
        Xeger xeger = new Xeger("ba?", new Random(8));
        java.lang.reflect.Method method = Xeger.class.getDeclaredMethod("appendRandomChoice", StringBuilder.class, Class.forName("dk.brics.automaton.State"), int.class, int.class);
        method.setAccessible(true);
        // setup for state, different regex from the original test
        dk.brics.automaton.State st = new dk.brics.automaton.RegExp("b?a").toAutomaton().getInitialState();
        Object result = method.invoke(xeger, new StringBuilder(), st, 0, 0);
        assertNotNull(result);
    }
}