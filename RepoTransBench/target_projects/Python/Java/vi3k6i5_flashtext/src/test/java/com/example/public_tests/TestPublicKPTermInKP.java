package com.example.public_tests;

import com.example.flashtext.KeywordProcessor;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class TestPublicKPTermInKP {
    @Test
    void testKPContainsKeyword() {
        KeywordProcessor kp = new KeywordProcessor();
        kp.add_keyword("java");
        assertTrue(kp.contains("java"));
        assertFalse(kp.contains("javascript"));
    }
}