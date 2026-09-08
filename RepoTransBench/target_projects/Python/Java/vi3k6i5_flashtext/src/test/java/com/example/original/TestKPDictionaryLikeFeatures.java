package com.example.original;

import com.example.flashtext.KeywordProcessor;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class TestKPDictionaryLikeFeatures {
    @Test
    void test_term_in_dictionary() {
        KeywordProcessor kp = new KeywordProcessor();
        kp.add_keyword("j2ee", "Java");
        kp.add_keyword("colour", "color");
        kp.get_keyword("j2ee");
        assertEquals("Java", kp.get_keyword("j2ee"));
        assertEquals("color", kp.get_keyword("colour"));
        assertNull(kp.get_keyword("Test"));
        assertTrue(kp.contains("colour"));
        assertFalse(kp.contains("Test"));
    }

    @Test
    void test_term_in_dictionary_case_sensitive() {
        KeywordProcessor kp = new KeywordProcessor(true);
        kp.add_keyword("j2ee", "Java");
        kp.add_keyword("colour", "color");
        kp.get_keyword("j2ee");
        assertEquals("Java", kp.get_keyword("j2ee"));
        assertEquals("color", kp.get_keyword("colour"));
        assertNull(kp.get_keyword("J2ee"));
        assertTrue(kp.contains("colour"));
        assertFalse(kp.contains("Colour"));
    }
}