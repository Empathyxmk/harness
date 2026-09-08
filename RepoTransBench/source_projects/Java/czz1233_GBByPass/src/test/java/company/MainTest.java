package company;

import org.junit.Test;
import static org.junit.Assert.*;

public class MainTest {
    @Test
    public void testReverseIfNotBlank_nonBlank() {
        assertEquals("321", Main.reverseIfNotBlank("123"));
        assertEquals("a", Main.reverseIfNotBlank("a"));
    }
    @Test
    public void testReverseIfNotBlank_blank() {
        assertEquals("", Main.reverseIfNotBlank(""));
        assertEquals("   ", Main.reverseIfNotBlank("   "));
    }
    @Test
    public void testIsAllDigits_numeric() {
        assertTrue(Main.isAllDigits("123456"));
    }
    @Test
    public void testIsAllDigits_nonNumeric() {
        assertFalse(Main.isAllDigits("abc"));
        assertFalse(Main.isAllDigits("123abc"));
        assertFalse(Main.isAllDigits(""));
        assertFalse(Main.isAllDigits("   "));
    }
    @Test
    public void testMain_withArgs() {
        // Since main prints to stdout, we just invoke it for coverage
        Main.main(new String[]{"123"});
        Main.main(new String[]{"abc"});
        Main.main(new String[]{""});
    }
}