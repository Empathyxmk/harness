package com.example.original;

import com.example.flashtext.KeywordProcessor;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.io.*;
import java.nio.file.*;
import java.util.*;

class TestRemoveKeywords {
    List<Map<String, Object>> testCases;

    @BeforeEach
    void setUp() throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        File jsonFile = Paths.get("test", "keyword_remover_test_cases.json").toFile();
        testCases = mapper.readValue(jsonFile, List.class);
    }

    @Test
    void test_remove_keywords() {
        int id = 0;
        for (Map<String, Object> testCase : testCases) {
            KeywordProcessor kp = new KeywordProcessor();
            Map<String, List<String>> keywordDict = (Map<String, List<String>>) testCase.get("keyword_dict");
            Map<String, List<String>> removeDict = (Map<String, List<String>>) testCase.get("remove_keyword_dict");
            kp.add_keywords_from_dict(keywordDict);
            kp.remove_keywords_from_dict(removeDict);
            String sentence = (String)testCase.get("sentence");
            List<String> expected = (List<String>) testCase.get("keywords");
            List<String> found = kp.extract_keywords(sentence);
            assertEquals(expected, found, "keywords_extracted don't match the expected results for test case: " + id);
            id++;
        }
    }

    @Test
    void test_remove_keywords_using_list() {
        int id = 0;
        for (Map<String, Object> testCase : testCases) {
            KeywordProcessor kp = new KeywordProcessor();
            Map<String, List<String>> keywordDict = (Map<String, List<String>>) testCase.get("keyword_dict");
            Map<String, List<String>> removeDict = (Map<String, List<String>>) testCase.get("remove_keyword_dict");
            kp.add_keywords_from_dict(keywordDict);
            for (String key : removeDict.keySet()) {
                kp.remove_keywords_from_list(removeDict.get(key));
            }
            String sentence = (String)testCase.get("sentence");
            List<String> expected = (List<String>) testCase.get("keywords");
            List<String> found = kp.extract_keywords(sentence);
            assertEquals(expected, found, "keywords_extracted don't match the expected results for test case: " + id);
            id++;
        }
    }

    @Test
    void test_remove_keywords_dictionary_compare() {
        int id = 0;
        for (Map<String, Object> testCase : testCases) {
            KeywordProcessor kp = new KeywordProcessor();
            Map<String, List<String>> keywordDict = (Map<String, List<String>>) testCase.get("keyword_dict");
            Map<String, List<String>> removeDict = (Map<String, List<String>>) testCase.get("remove_keyword_dict");
            kp.add_keywords_from_dict(keywordDict);
            kp.remove_keywords_from_dict(removeDict);

            // Simulate internal state checks between two processors after removal
            Map<String, List<String>> newDict = new HashMap<>();
            for (Map.Entry<String, List<String>> entry : keywordDict.entrySet()) {
                List<String> filtered = new ArrayList<>(entry.getValue());
                if (removeDict.containsKey(entry.getKey())) {
                    filtered.removeAll(removeDict.get(entry.getKey()));
                }
                newDict.put(entry.getKey(), filtered);
            }
            KeywordProcessor kp2 = new KeywordProcessor();
            kp2.add_keywords_from_dict(newDict);
            // Use custom equals method or serialize the trie for a real state comparison
            assertEquals(kp.toString(), kp2.toString(), "keywords_extracted don't match the expected results for test case: " + id);
            id++;
        }
    }
}