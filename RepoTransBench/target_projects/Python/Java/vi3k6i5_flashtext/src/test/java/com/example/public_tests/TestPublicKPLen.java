package com.example.public_tests;

import com.example.flashtext.KeywordProcessor;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class TestPublicKPLen {
    @Test
    void testKPLen() {
        KeywordProcessor kp = new KeywordProcessor();
        assertEquals(0, kp.length());
        kp.add_keyword("java", "java_2e");
        assertEquals(1, kp.length());
        kp.add_keyword("product management", "product manager");
        assertEquals(2, kp.length());
        kp.remove_keyword("java");
        assertEquals(1, kp.length());
    }
}