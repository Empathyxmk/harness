package com.seatgeek.original;

import com.seatgeek.fuzzywuzzy.Fuzz;
import com.seatgeek.fuzzywuzzy.Utils;
import com.seatgeek.fuzzywuzzy.StringProcessing;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class FuzzywuzzyTest {

    @Test
    void testReplaceNonLettersNonNumbersWithWhitespace() {
        String sample = "foo *$%# bar";
        String replaced = StringProcessing.replaceNonLettersNonNumbersWithWhitespace(sample);
        assertFalse(replaced.contains("*"));
        assertFalse(replaced.contains("$"));
        assertFalse(replaced.contains("%"));
        assertFalse(replaced.contains("#"));
        assertTrue(replaced.contains("foo"));
        assertTrue(replaced.contains("bar"));
    }

    @Test
    void testRatio() {
        assertEquals(100, Fuzz.ratio("foo", "foo"));
        assertTrue(Fuzz.ratio("foo", "food") < 100);
        assertEquals(0, Fuzz.ratio("abc", ""));
        assertEquals(0, Fuzz.ratio("", "abc"));
    }

    @Test
    void testPartialRatio() {
        assertEquals(100, Fuzz.partialRatio("foo", "food"));
        assertTrue(Fuzz.partialRatio("foo", "fod") < 100);
    }

    @Test
    void testTokenSortRatio() {
        assertEquals(100, Fuzz.tokenSortRatio("foo bar", "bar foo"));
        assertTrue(Fuzz.tokenSortRatio("foo bar", "foo boo") < 100);
    }

    @Test
    void testPartialTokenSortRatio() {
        assertEquals(100, Fuzz.partialTokenSortRatio("foo bar", "foo the bar"));
        assertTrue(Fuzz.partialTokenSortRatio("foo bar", "foo the boo") < 100);
    }

    @Test
    void testTokenSetRatio() {
        assertEquals(100, Fuzz.tokenSetRatio("foo bar", "bar foo"));
        assertEquals(100, Fuzz.tokenSetRatio("foo bar foo", "bar foo"));
        assertTrue(Fuzz.tokenSetRatio("foo bar", "foo boo") < 100);
    }

    @Test
    void testPartialTokenSetRatio() {
        assertEquals(100, Fuzz.partialTokenSetRatio("foo bar", "foo the bar boo"));
        assertTrue(Fuzz.partialTokenSetRatio("foo bar", "foo the boo barz") < 100);
    }

    @Test
    void testQRatio() {
        assertEquals(100, Fuzz.QRatio("foo", "foo"));
        assertEquals(100, Fuzz.QRatio("foo", "FOO"));
        assertTrue(Fuzz.QRatio("foo", "food") < 100);
    }

    @Test
    void testWRatio() {
        assertEquals(100, Fuzz.WRatio("foo", "foo"));
        assertEquals(100, Fuzz.WRatio("foo", "FOO"));
        assertTrue(Fuzz.WRatio("foo", "food") < 100);
    }

    @Test
    void testAsciidammit() {
        String unicodeStr = "Café Noël Über ß";
        String result = Utils.asciidammit(unicodeStr);
        assertNotNull(result);
        assertFalse(result.contains("é"));
        assertFalse(result.contains("ü"));
        assertFalse(result.contains("ß"));
    }

    @Test
    void testFullProcess() {
        String s = " A \t strIng With !@#$% weird chars & CAPS ";
        assertNotNull(Utils.fullProcess(s));
        assertNotNull(Utils.fullProcess(s, true));
    }
}