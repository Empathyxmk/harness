package com.manning.junitbook.ch02.parametrized;

import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import static org.junit.jupiter.api.Assertions.assertEquals;

class ParameterizedWithValueSourcePublicTest {
    private WordCounter wordCounter = new WordCounter();

    @ParameterizedTest
    @ValueSource(strings = {"New public test", "OpenAI model"})
    void testWordsInSentencePublic(String sentence) {
        assertEquals(3, wordCounter.countWords(sentence));
    }
}