package com.example.original;

import com.example.flashtext.KeywordProcessor;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class TestKPExceptions {
    @Test
    void test_iterator_NotImplementedError() {
        KeywordProcessor kp = new KeywordProcessor();
        kp.add_keyword("j2ee", "Java");
        kp.add_keyword("colour", "color");
        assertThrows(UnsupportedOperationException.class, () -> {
            // Try to iterate the object - should throw
            for (Object o : (Iterable<?>)kp) {
                // no-op
            }
        });
    }

    @Test
    void test_add_keyword_file_missing() {
        KeywordProcessor kp = new KeywordProcessor();
        assertThrows(java.io.IOException.class, () -> {
            kp.add_keyword_from_file("missing_file");
        });
    }

    @Test
    void test_add_keyword_from_list_type_error() {
        KeywordProcessor kp = new KeywordProcessor();
        assertThrows(ClassCastException.class, () -> {
            kp.add_keywords_from_list((List<String>)(Object)"java");
        });
    }

    @Test
    void test_add_keyword_from_dictionary_type_error() {
        KeywordProcessor kp = new KeywordProcessor();
        Map<String, String> invalidDict = new HashMap<>();
        invalidDict.put("java", "java_2e");
        invalidDict.put("product management", "product manager");
        assertThrows(ClassCastException.class, () -> {
            kp.add_keywords_from_dict((Map<String, List<String>>)(Object)invalidDict);
        });
    }

    @Test
    void test_remove_keyword_from_list_type_error() {
        KeywordProcessor kp = new KeywordProcessor();
        assertThrows(ClassCastException.class, () -> {
            kp.remove_keywords_from_list((List<String>)(Object)"java");
        });
    }

    @Test
    void test_remove_keyword_from_dictionary_type_error() {
        KeywordProcessor kp = new KeywordProcessor();
        Map<String, String> invalidDict = new HashMap<>();
        invalidDict.put("java", "java_2e");
        invalidDict.put("product management", "product manager");
        assertThrows(ClassCastException.class, () -> {
            kp.remove_keywords_from_dict((Map<String, List<String>>)(Object)invalidDict);
        });
    }

    @Test
    void test_empty_string() {
        KeywordProcessor kp = new KeywordProcessor();
        assertEquals(Collections.emptyList(), kp.extract_keywords(""));
        assertEquals("", kp.replace_keywords(""));
    }
}