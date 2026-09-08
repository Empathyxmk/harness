package com.example.original;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.text.Normalizer;
import java.util.HashSet;
import java.util.Set;

public class TestUuslug {

    private Set<String> existingSlugs;

    @BeforeEach
    void setUp() {
        existingSlugs = new HashSet<>();
    }

    /**
     * Simulate uuslug.slugify function. This version tries to mimic the slugification
     * behavior from the Python version, including uniqueness on request.
     */
    String slugify(String source, String allowUnicode, boolean ensureUnique) {
        if (source == null) return "";
        String slug;
        if ("True".equalsIgnoreCase(allowUnicode)) {
            // Allow unicode: keep unicode chars, but normalize spaces and punctuation.
            slug = source.trim()
                    .replaceAll("[\\s_]+", "-")
                    .replaceAll("[\\p{Punct}&&[^-]]+", "")
                    .replaceAll("-+", "-");
        } else {
            // Remove accents, keep ascii only.
            slug = Normalizer.normalize(source, Normalizer.Form.NFD)
                    .replaceAll("[^\\p{ASCII}]", "")
                    .replaceAll("[^\\w\\s-]", "")
                    .replaceAll("_", "-")
                    .replaceAll("\\s+", "-")
                    .replaceAll("-+", "-")
                    .toLowerCase();
        }
        slug = slug.replaceAll("^-+|-+$", "");

        if (!ensureUnique) return slug;

        String uniqueSlug = slug;
        int count = 1;
        while (existingSlugs.contains(uniqueSlug)) {
            uniqueSlug = slug + "-" + count;
            count++;
        }
        existingSlugs.add(uniqueSlug);
        return uniqueSlug;
    }

    @Test
    void testBasicSlugify() {
        assertEquals("hello-world", slugify("Hello world!", "False", false));
        assertEquals("winter-is-coming", slugify("Winter is coming.", "False", false));
        assertEquals("test", slugify("test", "False", false));
    }

    @Test
    void testSlugifyWithUnicodeAllowed() {
        // Should allow unicode, but preserve sluggification.
        String slug = slugify("Zażółć gęślą jaźń", "True", false);
        assertTrue(slug.contains("Zażółć") || slug.contains("ż") || slug.contains("ń")); // demonstration
        String slugAscii = slugify("Zażółć gęślą jaźń", "False", false);
        assertFalse(slugAscii.contains("ż"));
        assertFalse(slugAscii.contains("ń"));
    }

    @Test
    void testSlugifyEnsureUnique() {
        String s1 = slugify("Repeat Me", "False", true);
        assertEquals("repeat-me", s1);
        String s2 = slugify("Repeat Me", "False", true);
        assertEquals("repeat-me-1", s2);
        String s3 = slugify("Repeat Me", "False", true);
        assertEquals("repeat-me-2", s3);
    }

    @Test
    void testEdgeCases() {
        assertEquals("", slugify("", "False", false));
        assertEquals("", slugify(" ", "False", false));
        assertEquals("123", slugify("123", "False", false));
        assertEquals("n-a", slugify("n/a", "False", false));
        assertEquals("abc", slugify("  abc  ", "False", false));
    }

    @Test
    void testLongUniqueSlug() {
        String s1 = slugify("MyTestSlugWithLongString", "False", true);
        assertEquals("mytestslugwithlongstring", s1);
        String s2 = slugify("MyTestSlugWithLongString", "False", true);
        assertEquals("mytestslugwithlongstring-1", s2);
    }

    @Test
    void testSeparatorBehavior() {
        // This version uses only hyphen for separator
        assertEquals("foo-bar", slugify("foo bar", "False", false));
    }
}