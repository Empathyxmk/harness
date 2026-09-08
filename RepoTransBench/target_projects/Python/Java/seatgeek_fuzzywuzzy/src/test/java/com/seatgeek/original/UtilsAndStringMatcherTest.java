package com.seatgeek.original;

import com.seatgeek.fuzzywuzzy.Utils;
import com.seatgeek.fuzzywuzzy.StringProcessing;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class UtilsAndStringMatcherTest {

    @Test
    void testValidateStringStrAndNone() {
        // Should return true for string input
        assertTrue(Utils.validateString("abc"));
        // Should return false for null
        assertFalse(Utils.validateString(null));
        // Should return false for non-string input
        assertFalse(Utils.validateString(123));
        assertFalse(Utils.validateString(new int[] {}));
    }

    @Test
    void testMakeTypeConsistentStr() {
        Object[] res = Utils.makeTypeConsistent("abc", "def");
        assertTrue(res[0] instanceof String && res[1] instanceof String);
    }

    @Test
    void testIntrBehavior() {
        // Should round to nearest integer using Java Math.round
        assertEquals(4, Utils.intr(3.7));
        assertEquals(3, Utils.intr(3.3));
        // Should throw for String input
        assertThrows(ClassCastException.class, () -> { Utils.intr("42"); });
    }

    @Test
    void testAsciidammitAscii() {
        assertEquals("hello", Utils.asciidammit("hello"));
    }

    @Test
    void testAsciionlyBasic() {
        assertEquals("TeSt", Utils.asciionly("TeSt"));
        // asciionly will not filter out unicode by default
        assertEquals("abc✓", Utils.asciionly("abc✓"));
    }

    @Test
    void testFullProcessOptions() {
        String s = " This is Ünicode!   ";
        String processed = Utils.fullProcess(s);
        // It preserves ü, so match on substring with/without accent
        assertTrue(processed.toLowerCase().contains("ünicod"));

        String processedAscii = Utils.fullProcess(s, true);
        assertTrue(processedAscii.toLowerCase().contains("nicode"));

        assertEquals("", Utils.fullProcess("", true));
        assertEquals("", Utils.fullProcess("   "));
    }

    @Test
    void testStripAndCase() {
        String s = "  hello\n";
        assertEquals(s.strip(), StringProcessing.strip(s));
        assertEquals(s.toLowerCase(), StringProcessing.toLowerCase(s));
        assertEquals(s.toUpperCase(), StringProcessing.toUpperCase(s));
    }
}