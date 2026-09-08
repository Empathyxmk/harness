package com.example.public_tests;

import com.example.flashtext.KeywordProcessor;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class TestPublicExtractFuzzy {
    @Test
    void testExtractDeletion() {
        KeywordProcessor keywordProc = new KeywordProcessor();
        keywordProc.add_keyword("skype", "messenger");
        String sentence = "hello, do you have skpe ?";
        List<String> expected = Arrays.asList("skype");
        assertEquals(expected, keywordProc.extract_keywords(sentence, 1));
    }

    @Test
    void testExtractInsertion() {
        KeywordProcessor keywordProc = new KeywordProcessor();
        keywordProc.add_keyword("ebay");
        String sentence = "ebaaaay is the best";
        List<String> expected = Arrays.asList("ebay");
        assertEquals(expected, keywordProc.extract_keywords(sentence, 2));
    }

    @Test
    void testExtractCostSpreadMultipleWords() {
        KeywordProcessor keywordProc = new KeywordProcessor();
        keywordProc.add_keyword("made of multiple words");
        String sentence = "this sentence contains a keyword maade of multple words";
        List<String> expected = Arrays.asList("made of multiple words");
        assertEquals(expected, keywordProc.extract_keywords(sentence, 2));
    }
}