package com.manning.junitbook.ch02.parametrized;

import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import static org.junit.jupiter.api.Assertions.assertEquals;

class ParameterizedWithCsvSourcePublicTest {
    private WordCounter wordCounter = new WordCounter();

    @ParameterizedTest
    @CsvSource({
        "1, Hello", 
        "5, This is a public test", 
        "2, Hello World"
    })
    void testWordsInSentencePublic(int expected, String sentence) {
        assertEquals(expected, wordCounter.countWords(sentence));
    }
}