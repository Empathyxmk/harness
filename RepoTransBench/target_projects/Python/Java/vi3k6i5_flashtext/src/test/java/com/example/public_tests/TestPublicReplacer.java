package com.example.public_tests;

import com.example.flashtext.KeywordProcessor;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.io.*;
import java.nio.file.*;
import java.util.*;

class TestPublicReplacer {
    List<Map<String, Object>> testCases;

    @BeforeEach
    void setUp() throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        File jsonFile = Paths.get("test", "keyword_extractor_test_cases.json").toFile();
        testCases = mapper.readValue(jsonFile, List.class);
    }

    @Test
    void testReplaceKeywords() {
        int id = 0;
        for (Map<String, Object> testCase : testCases) {
            KeywordProcessor kp = new KeywordProcessor();
            Map<String, List<String>> keywordDict = (Map<String, List<String>>) testCase.get("keyword_dict");
            kp.add_keywords_from_dict(keywordDict);
            String sentence = (String)testCase.get("sentence");
            String expected = (String) testCase.get("replace_keywords");
            String actual = kp.replace_keywords(sentence);
            assertEquals(expected, actual, "replace_keywords doesn't match the expected result for test case: " + id);
            id++;
        }
    }
}