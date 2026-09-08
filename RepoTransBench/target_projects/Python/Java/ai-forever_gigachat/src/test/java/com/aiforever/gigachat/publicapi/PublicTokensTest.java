package com.aiforever.gigachat.publicapi;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class TokenCounter {
    int countTokens(String s) {
        return s.trim().isEmpty() ? 0 : s.trim().split("\\s+").length;
    }
}

public class PublicTokensTest {
    @Test
    void testTokenCounting() {
        TokenCounter tc = new TokenCounter();
        assertEquals(4, tc.countTokens("This is a test"));
        assertEquals(3, tc.countTokens("foo bar baz"));
    }

    @Test
    void testTokenCountingEmpty() {
        TokenCounter tc = new TokenCounter();
        assertEquals(0, tc.countTokens(""));
        assertEquals(0, tc.countTokens("     "));
    }
}