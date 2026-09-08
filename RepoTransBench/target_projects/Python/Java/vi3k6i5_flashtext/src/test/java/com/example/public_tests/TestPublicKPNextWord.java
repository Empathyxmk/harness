package com.example.public_tests;

import com.example.flashtext.KeywordProcessor;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class TestPublicKPNextWord {
    @Test
    void testNextWord() {
        KeywordProcessor kp = new KeywordProcessor();
        assertEquals("", kp.get_next_word(""));
        assertEquals("random", kp.get_next_word("random sentence"));
        assertEquals("", kp.get_next_word(" random sentence"));
    }
}