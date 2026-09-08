package com.example.public_tests;

import com.example.flashtext.KeywordProcessor;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class TestPublicKPExceptions {
    @Test
    void testRemoveKeywordFromListTypeError() {
        KeywordProcessor kp = new KeywordProcessor();
        assertThrows(ClassCastException.class, () -> {
            kp.remove_keywords_from_list((List<String>)(Object)"java");
        });
    }

    @Test
    void testRemoveKeywordFromDictTypeError() {
        KeywordProcessor kp = new KeywordProcessor();
        Map<String, String> invalidDict = new HashMap<>();
        invalidDict.put("java", "java_2e");
        assertThrows(ClassCastException.class, () -> {
            kp.remove_keywords_from_dict((Map<String, List<String>>)(Object)invalidDict);
        });
    }
}