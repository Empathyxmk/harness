package company;

import org.junit.Test;
import static org.junit.Assert.*;

public class MainPublicTest {
    @Test
    public void testReverseIfNotBlank_nonBlank() {
        // Different values than original: use "abcde" → "edcba", and "Z"
        assertEquals("edcba", Main.reverseIfNotBlank("abcde"));
        assertEquals("Z", Main.reverseIfNotBlank("Z"));
    }
    @Test
    public void testReverseIfNotBlank_blank() {
        // Use tab string and a multi-space string
        assertEquals("\t", Main.reverseIfNotBlank("\t"));
        assertEquals("    ", Main.reverseIfNotBlank("    "));
    }
    @Test
    public void testIsAllDigits_numeric() {
        // Use different digit string
        assertTrue(Main.isAllDigits("987654"));
    }
    @Test
    public void testIsAllDigits_nonNumeric() {
        assertFalse(Main.isAllDigits("def"));
        assertFalse(Main.isAllDigits("789ghi"));
        assertFalse(Main.isAllDigits("")); // edge (but already in original, needs to be kept)
        assertFalse(Main.isAllDigits("    "));
    }
    @Test
    public void testMain_withArgs() {
        // Different args for coverage
        Main.main(new String[]{"456"});
        Main.main(new String[]{"def"});
        Main.main(new String[]{" "});
    }
}