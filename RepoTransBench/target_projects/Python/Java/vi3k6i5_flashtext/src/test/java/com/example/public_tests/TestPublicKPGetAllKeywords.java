package com.example.public_tests;

import com.example.flashtext.KeywordProcessor;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class TestPublicKPGetAllKeywords {
    @Test
    void testGetAllKeywords() {
        KeywordProcessor kp = new KeywordProcessor();
        kp.add_keyword("j2ee", "Java");
        kp.add_keyword("colour", "color");
        Map<String, String> result = kp.get_all_keywords();
        Map<String, String> expected = new HashMap<>();
        expected.put("colour", "color");
        expected.put("j2ee", "Java");
        assertEquals(expected, result, "get_all_keywords didn't match expected results.");
    }
}