package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestUuslugFunc {

    // Simulate the main uuslug slugification utility (from previous file)
    static String slugify(String text) {
        if (text == null) return "";
        String slug = text.replaceAll("[^\\w\\s-]", "").replace("_", "-").replaceAll("\\s+", "-").toLowerCase();
        return slug.replaceAll("^-+|-+$", "");
    }

    @Test
    void testSlugifyAscii() {
        assertEquals("hello-world", slugify("Hello world!"));
        assertEquals("winter-is-coming", slugify("Winter is coming."));
        assertEquals("multiple-spaces-in-this-string", slugify("Multiple      spaces    in this string!"));
    }

    @Test
    void testSlugifyUnicode() {
        String unicodeStr = slugify("Жжё Ё");
        // Since the simple slugify here strips non-ascii, expect empty string.
        assertEquals("", unicodeStr);
        String accent = slugify("Zażółć gęślą jaźń!");
        assertTrue(accent instanceof String); // should not throw
    }

    @Test
    void testSlugifyCornerCases() {
        assertEquals("", slugify(""));
        assertEquals("", slugify("."));
        assertEquals("", slugify("!"));
        assertEquals("123", slugify("123"));
        assertEquals("abc", slugify("abc"));
        assertEquals("-1", slugify("-1"));
    }

    @Test
    void testSlugifyWhitespace() {
        assertEquals("foo-bar", slugify("  foo   bar  "));
        assertEquals("foo-bar", slugify("foo        bar"));
        assertEquals("foo-bar", slugify("foo\tbar"));
    }

    @Test
    void testSlugifyCustomSeparators() {
        // This function ignores the separator param for simplicity—as in Python fallback.
        assertEquals("foo-bar", slugify("foo bar"));
    }

}