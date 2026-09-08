package com.manning.junitbook.ch02.parametrized;

import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvFileSource;

import static org.junit.jupiter.api.Assertions.assertEquals;

class ParameterizedWithCsvFileSourcePublicTest {
    private WordCounter wordCounter = new WordCounter();

    @ParameterizedTest
    @CsvFileSource(resources = "/word_counter_public.csv")
    void testWordsInSentencePublic(int expected, String sentence) {
        assertEquals(expected, wordCounter.countWords(sentence));
    }
}