package nl.flotsam.xeger;

import org.junit.Test;
import static org.junit.Assert.*;

public class XegerPublicTest {

    @Test
    public void testLiteralGeneration() {
        String regex = "abcXYZ";
        Xeger generator = new Xeger(regex);
        String result = generator.generate();
        assertEquals("abcXYZ", result);
    }

    @Test
    public void testSimpleDigitGeneration() {
        String regex = "[4-6]{4}";
        Xeger generator = new Xeger(regex);
        String result = generator.generate();
        assertEquals(4, result.length());
        assertTrue(result.matches("[4-6]{4}"));
    }

    @Test
    public void testSimpleAlphaGeneration() {
        String regex = "[A-C]{3}";
        Xeger generator = new Xeger(regex);
        String result = generator.generate();
        assertEquals(3, result.length());
        assertTrue(result.matches("[A-C]{3}"));
    }

    @Test
    public void testRangeWithSpecialChar() {
        String regex = "[M-Q]{2}-[7-9]{2}";
        Xeger generator = new Xeger(regex);
        String str = generator.generate();
        assertTrue(str.matches("[M-Q]{2}-[7-9]{2}"));
    }

    @Test
    public void testRandomNumericGeneration() {
        // Choose a pattern and valid assertion that will always pass
        String regex = "[98]{8}";
        Xeger generator = new Xeger(regex);
        String str = generator.generate();
        assertEquals(8, str.length());
        assertTrue(str.matches("[98]{8}"));
    }

}