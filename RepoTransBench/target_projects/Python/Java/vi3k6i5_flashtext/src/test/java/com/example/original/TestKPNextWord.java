package com.example.original;

import com.example.flashtext.KeywordProcessor;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class TestKPNextWord {
    @Test
    void test_next_word() {
        KeywordProcessor kp = new KeywordProcessor();
        assertEquals("", kp.get_next_word(""));
        assertEquals("random", kp.get_next_word("random sentence"));
        assertEquals("", kp.get_next_word(" random sentence"));
    }
}