package com.example.original;

import com.example.flashtext.KeywordProcessor;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.io.*;
import java.nio.file.*;
import java.util.*;

@TestMethodOrder(MethodOrderer.MethodName.class)
class TestKPLen {
    List<Map<String, Object>> testCases;

    @BeforeEach
    void setUp() throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        File jsonFile = Paths.get("test", "keyword_remover_test_cases.json").toFile();
        testCases = mapper.readValue(jsonFile, List.class);
    }

    @Test
    void test_remove_keywords_dictionary_len() {
        int id = 0;
        for (Map<String, Object> testCase : testCases) {
            KeywordProcessor kp1 = new KeywordProcessor();
            Map<String, List<String>> keywordDict = (Map<String, List<String>>) testCase.get("keyword_dict");
            Map<String, List<String>> removeDict = (Map<String, List<String>>) testCase.get("remove_keyword_dict");
            kp1.add_keywords_from_dict(keywordDict);
            kp1.remove_keywords_from_dict(removeDict);

            int len1 = kp1.len();

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
            int len2 = kp2.len();
            assertEquals(len1, len2, "keyword processor length doesn't match for Text ID " + id);
            id++;
        }
    }
}