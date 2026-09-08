package com.example.original;

import com.example.flashtext.KeywordProcessor;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class TestLoadingKeywordList {
    @Test
    void test_list_loading() {
        KeywordProcessor kp = new KeywordProcessor();
        List<String> keywordList = Arrays.asList("java", "product management");
        kp.add_keywords_from_list(keywordList);
        String sentence = "I know java and product management";
        assertEquals(Arrays.asList("java", "product management"), kp.extract_keywords(sentence));
        String replaced = kp.replace_keywords(sentence);
        assertEquals("I know java and product management", replaced);
    }
}