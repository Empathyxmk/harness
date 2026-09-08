package com.example.public_tests;

import com.example.flashtext.KeywordProcessor;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class TestPublicDictionaryLoading {
    @Test
    void testPublicDictionaryLoading() {
        KeywordProcessor kp = new KeywordProcessor();
        Map<String, List<String>> keywordDict = new HashMap<>();
        keywordDict.put("java", Arrays.asList("java_2e", "java programing"));
        keywordDict.put("product management", Arrays.asList("product management techniques", "product management"));
        kp.add_keywords_from_dict(keywordDict);
        String sentence = "I know java_2e and product management techniques";
        List<String> keywordsExtracted = kp.extract_keywords(sentence);
        assertEquals(Arrays.asList("java", "product management"), keywordsExtracted);
        String sentenceNew = kp.replace_keywords(sentence);
        assertEquals("I know java and product management", sentenceNew);
    }
}