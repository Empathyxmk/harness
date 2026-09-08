package com.example.original;

import com.example.flashtext.KeywordProcessor;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class TestReplaceFuzzy {
    @Test
    void test_extract_deletion() {
        KeywordProcessor keywordProc = new KeywordProcessor();
        keywordProc.add_keyword("skype", "messenger");
        String sentence = "hello, do you have skpe ?";
        String targetSentence = "hello, do you have messenger ?";
        assertEquals(targetSentence, keywordProc.replace_keywords(sentence, 1));
    }

    @Test
    void test_replace_addition() {
        KeywordProcessor keywordProc = new KeywordProcessor();
        keywordProc.add_keyword("colour here", "couleur ici");
        keywordProc.add_keyword("and heere", "et ici");
        String sentence = "color here blabla and here";
        String targetSentence = "couleur ici blabla et ici";
        assertEquals(targetSentence, keywordProc.replace_keywords(sentence, 1));
    }

    @Test
    void test_replace_cost_spread_over_multiple_words() {
        KeywordProcessor keywordProc = new KeywordProcessor();
        keywordProc.add_keyword("made of multiple words", "with only one word");
        String sentence = "this sentence contains a keyword maade of multple words";
        String targetSentence = "this sentence contains a keyword with only one word";
        assertEquals(targetSentence, keywordProc.replace_keywords(sentence, 2));
    }

    @Test
    void test_replace_multiple_keywords() {
        KeywordProcessor keywordProc = new KeywordProcessor();
        keywordProc.add_keyword("first keyword", "1st keyword");
        keywordProc.add_keyword("second keyword", "2nd keyword");
        String sentence = "start with a first kyword then add a secand keyword";
        String targetSentence = "start with a 1st keyword then add a 2nd keyword";
        assertEquals(targetSentence, keywordProc.replace_keywords(sentence, 1));
    }

    @Test
    void test_intermediate_match_then_no_match() {
        KeywordProcessor keywordProc = new KeywordProcessor();
        keywordProc.add_keyword("keyword");
        keywordProc.add_keyword("keyword with many words");
        String sentence = "This sentence contains a keywrd with many items inside, A keyword at the end";
        String targetSentence = "This sentence contains a keyword with many items inside, A keyword at the end";
        assertEquals(targetSentence, keywordProc.replace_keywords(sentence, 1));
    }

    @Test
    void test_special_symbol() {
        KeywordProcessor keywordProc = new KeywordProcessor();
        keywordProc.add_keyword("No. of Colors", "Número de colores");
        String sentence = "No. of colours: 10";
        String targetSentence = "Número de colores: 10";
        assertEquals(targetSentence, keywordProc.replace_keywords(sentence, 2));
    }
}