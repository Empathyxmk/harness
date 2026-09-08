package com.example.original;

import com.example.flashtext.KeywordProcessor;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.io.*;

class TestFileLoad {

    @Test
    void test_file_format_one() {
        KeywordProcessor kp = new KeywordProcessor();
        // Assume integration with test keywords file,
        // In real tests, the file has to be populated in the test resources.
        kp.add_keyword_from_file("test/keywords_format_one.txt");
        String sentence = "I know java_2e and product management techniques";
        assertEquals(List.of("java", "product management"), kp.extract_keywords(sentence));
        String sentenceNew = kp.replace_keywords(sentence);
        assertEquals("I know java and product management", sentenceNew);
    }

    @Test
    void test_file_format_two() {
        KeywordProcessor kp = new KeywordProcessor();
        kp.add_keyword_from_file("test/keywords_format_two.txt");
        String sentence = "I know java and product management";
        assertEquals(List.of("java", "product management"), kp.extract_keywords(sentence));
        String sentenceNew = kp.replace_keywords(sentence);
        assertEquals("I know java and product management", sentenceNew);
    }
}