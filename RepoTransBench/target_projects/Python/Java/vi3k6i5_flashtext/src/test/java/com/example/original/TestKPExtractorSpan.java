package com.example.original;

import com.example.flashtext.KeywordProcessor;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.io.*;
import java.nio.file.*;
import java.util.*;

class TestKPExtractorSpan {
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
            for (String key : keywordDict.keySet()) {
                kp.add_keywords_from_list(keywordDict.get(key));
            }
            String sentence = (String)testCase.get("sentence");
            List<Object[]> found = kp.extract_keywords(sentence, true);
            for (Object[] kwd : found) {
                String kw = ((String)kwd[0]).toLowerCase();
                String substr = sentence.toLowerCase().substring((int)kwd[1], (int)kwd[2]);
                assertEquals(kw, substr, "keywords span don't match the expected results for test case: " + id);
            }
            id++;
        }
    }

    @Test
    void test_extract_keywords_case_sensitive() {
        int id = 0;
        for (Map<String, Object> testCase : testCases) {
            KeywordProcessor kp = new KeywordProcessor(true);
            Map<String, List<String>> keywordDict = (Map<String, List<String>>) testCase.get("keyword_dict");
            for (String key : keywordDict.keySet()) {
                kp.add_keywords_from_list(keywordDict.get(key));
            }
            String sentence = (String)testCase.get("sentence");
            List<Object[]> found = kp.extract_keywords(sentence, true);
            for (Object[] kwd : found) {
                String kw = (String)kwd[0];
                String substr = sentence.substring((int)kwd[1], (int)kwd[2]);
                assertEquals(kw, substr, "keywords span don't match the expected results for test case: " + id);
            }
            id++;
        }
    }
}