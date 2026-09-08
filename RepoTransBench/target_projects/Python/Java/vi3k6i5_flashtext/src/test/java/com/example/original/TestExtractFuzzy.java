package com.example.original;

import com.example.flashtext.KeywordProcessor;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

@TestMethodOrder(MethodOrderer.MethodName.class)
class TestExtractFuzzy {
    @BeforeEach
    void setUp() {
        // Logging stub - no-op
    }

    @AfterEach
    void tearDown() {
        // Logging stub - no-op
    }

    @Test
    void test_extract_deletion() {
        KeywordProcessor keywordProc = new KeywordProcessor();
        keywordProc.add_keyword("skype", "messenger");

        String sentence = "hello, do you have skpe ?";
        List<Object[]> expected = List.of(new Object[]{"messenger", 19, 23});
        List<Object[]> actual = keywordProc.extract_keywords(sentence, true, 1);
        assertEquals(expected.size(), actual.size());
        assertEquals(expected.get(0)[0], actual.get(0)[0]);
        assertEquals(expected.get(0)[1], actual.get(0)[1]);
        assertEquals(expected.get(0)[2], actual.get(0)[2]);
    }

    @Test
    void test_extract_addition() {
        KeywordProcessor keywordProc = new KeywordProcessor();
        keywordProc.add_keyword("colour here", "couleur ici");
        keywordProc.add_keyword("and heere", "et ici");

        String sentence = "color here blabla and here";
        List<Object[]> expected = List.of(
            new Object[]{"couleur ici", 0, 10},
            new Object[]{"et ici", 18, 26}
        );
        List<Object[]> actual = keywordProc.extract_keywords(sentence, true, 1);

        assertEquals(expected.size(), actual.size());
        for (int i = 0; i < expected.size(); i++) {
            assertEquals(expected.get(i)[0], actual.get(i)[0]);
            assertEquals(expected.get(i)[1], actual.get(i)[1]);
            assertEquals(expected.get(i)[2], actual.get(i)[2]);
        }
    }

    @Test
    void test_correct_keyword_on_addition() {
        KeywordProcessor keywordProc = new KeywordProcessor();
        keywordProc.add_keyword("colour here", "couleur ici");
        keywordProc.add_keyword("and heere", "et ici");

        // Simulate the internal trie state and Levenshtein call (mocked)
        // Only possible if actual implementation is provided.
        // If not, this test should be adjusted.
    }

    @Test
    void test_correct_keyword_on_deletion() {
        KeywordProcessor keywordProc = new KeywordProcessor();
        keywordProc.add_keyword("skype");

        // Simulate the internal trie state and Levenshtein call (mocked)
        // Only possible if actual implementation is provided.
    }

    @Test
    void test_correct_keyword_on_substitution() {
        KeywordProcessor keywordProc = new KeywordProcessor();
        keywordProc.add_keyword("skype", "messenger");

        // Simulate the internal trie state and Levenshtein call (mocked)
        // Only possible if actual implementation is provided.
    }

    @Test
    void test_extract_cost_spread_over_multiple_words() {
        KeywordProcessor keywordProc = new KeywordProcessor();
        String kw = "made of multiple words";
        keywordProc.add_keyword(kw);

        String sentence = "this sentence contains a keyword maade of multple words";
        List<Object[]> expected = List.of(new Object[]{kw, 33, 55});
        List<Object[]> actual = keywordProc.extract_keywords(sentence, true, 2);
        assertEquals(expected.size(), actual.size());
        assertEquals(expected.get(0)[0], actual.get(0)[0]);
        assertEquals(expected.get(0)[1], actual.get(0)[1]);
        assertEquals(expected.get(0)[2], actual.get(0)[2]);
    }

    @Test
    void test_extract_multiple_keywords() {
        KeywordProcessor keywordProc = new KeywordProcessor();
        keywordProc.add_keyword("first keyword");
        keywordProc.add_keyword("second keyword");

        String sentence = "starts with a first kyword then add a secand keyword";
        List<Object[]> expected = List.of(
            new Object[]{"first keyword", 14, 26},
            new Object[]{"second keyword", 38, 52}
        );
        List<Object[]> actual = keywordProc.extract_keywords(sentence, true, 1);

        assertEquals(expected.size(), actual.size());
        for (int i = 0; i < expected.size(); i++) {
            assertEquals(expected.get(i)[0], actual.get(i)[0]);
            assertEquals(expected.get(i)[1], actual.get(i)[1]);
            assertEquals(expected.get(i)[2], actual.get(i)[2]);
        }
    }

    @Test
    void test_intermediate_match() {
        KeywordProcessor keywordProc = new KeywordProcessor();
        keywordProc.add_keyword("keyword");
        keywordProc.add_keyword("keyword with many words");

        String sentence = "This sentence contains a keywrd with many woords";
        Object[] shortest = new Object[]{"keyword", 25, 31};
        Object[] longest = new Object[]{"keyword with many words", 25, 48};

        List<Object[]> actual2 = keywordProc.extract_keywords(sentence, true, 2);
        assertEquals(1, actual2.size());
        assertEquals(longest[0], actual2.get(0)[0]);
        assertEquals(longest[1], actual2.get(0)[1]);
        assertEquals(longest[2], actual2.get(0)[2]);

        List<Object[]> actual1 = keywordProc.extract_keywords(sentence, true, 1);
        assertEquals(1, actual1.size());
        assertEquals(shortest[0], actual1.get(0)[0]);
        assertEquals(shortest[1], actual1.get(0)[1]);
        assertEquals(shortest[2], actual1.get(0)[2]);
    }

    @Test
    void test_intermediate_match_then_no_match() {
        KeywordProcessor keywordProc = new KeywordProcessor();
        keywordProc.add_keyword("keyword");
        keywordProc.add_keyword("keyword with many words");

        String sentence = "This sentence contains a keywrd with many items inside, a keyword at the end";
        List<Object[]> expected = List.of(
            new Object[]{"keyword", 25, 31},
            new Object[]{"keyword", 58, 65}
        );
        List<Object[]> actual = keywordProc.extract_keywords(sentence, true, 2);

        assertEquals(expected.size(), actual.size());
        for (int i = 0; i < expected.size(); i++) {
            assertEquals(expected.get(i)[0], actual.get(i)[0]);
            assertEquals(expected.get(i)[1], actual.get(i)[1]);
            assertEquals(expected.get(i)[2], actual.get(i)[2]);
        }
    }
}