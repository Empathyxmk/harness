package com.example.original;

import com.example.flashtext.KeywordProcessor;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.io.*;
import java.nio.file.*;
import java.util.*;

class TestExtractor {
    List<Map<String, Object>> testCases;

    @BeforeEach
    void setUp() throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        File jsonFile = Paths.get("test", "keyword_extractor_test_cases.json").toFile();
        testCases = mapper.readValue(jsonFile, List.class);
    }

    @Test
    void test_extract_keywords() {
        int id = 0;
        for (Map<String, Object> testCase : testCases) {
            KeywordProcessor kp = new KeywordProcessor();
            Map<String, List<String>> keywordDict = (Map<String, List<String>>) testCase.get("keyword_dict");
            kp.add_keywords_from_dict(keywordDict);
            String sentence = (String)testCase.get("sentence");
            List<String> expected = (List<String>) testCase.get("keywords");
            List<String> found = kp.extract_keywords(sentence);
            assertEquals(expected, found, "keywords_extracted don't match the expected results for test case: " + id);
            id++;
        }
    }

    @Test
    void test_extract_keywords_case_sensitive() {
        int id = 0;
        for (Map<String, Object> testCase : testCases) {
            KeywordProcessor kp = new KeywordProcessor(true);
            Map<String, List<String>> keywordDict = (Map<String, List<String>>) testCase.get("keyword_dict");
            kp.add_keywords_from_dict(keywordDict);
            String sentence = (String)testCase.get("sentence");
            List<String> expected = (List<String>) testCase.get("keywords_case_sensitive");
            List<String> found = kp.extract_keywords(sentence);
            assertEquals(expected, found, "keywords_extracted don't match the expected results for test case: " + id);
            id++;
        }
    }
}