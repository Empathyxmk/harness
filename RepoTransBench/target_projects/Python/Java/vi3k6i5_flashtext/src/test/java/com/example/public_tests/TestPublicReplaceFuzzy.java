package com.example.public_tests;

import com.example.flashtext.KeywordProcessor;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class TestPublicReplaceFuzzy {
    @Test
    void testReplaceDeletion() {
        KeywordProcessor keywordProc = new KeywordProcessor();
        keywordProc.add_keyword("skype", "messenger");
        String sentence = "hello, do you have skpe ?";
        String targetSentence = "hello, do you have messenger ?";
        assertEquals(targetSentence, keywordProc.replace_keywords(sentence, 1));
    }

    @Test
    void testReplaceAddition() {
        KeywordProcessor keywordProc = new KeywordProcessor();
        keywordProc.add_keyword("colour here", "couleur ici");
        keywordProc.add_keyword("and heere", "et ici");
        String sentence = "color here blabla and here";
        String targetSentence = "couleur ici blabla et ici";
        assertEquals(targetSentence, keywordProc.replace_keywords(sentence, 1));
    }
}