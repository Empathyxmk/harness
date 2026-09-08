package com.example.public_tests;

import com.example.flashtext.KeywordProcessor;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class TestPublicFileLoad {
    @Test
    void testAddKeywordFromFile() throws Exception {
        KeywordProcessor kp = new KeywordProcessor();
        String filePath = "test/keywords_format_one.txt";
        kp.add_keyword_from_file(filePath);
        String sentence = "java_2e and product management techniques";
        assertEquals(Arrays.asList("java", "product management"), kp.extract_keywords(sentence));
        String replacedSentence = kp.replace_keywords(sentence);
        assertEquals("java and product management", replacedSentence);
    }
}