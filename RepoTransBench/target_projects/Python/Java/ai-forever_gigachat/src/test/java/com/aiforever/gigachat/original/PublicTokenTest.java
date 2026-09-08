package com.aiforever.gigachat.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class Token {
    String accessToken;
    long expiresIn;

    public Token(String accessToken, long expiresIn) {
        this.accessToken = accessToken;
        this.expiresIn = expiresIn;
    }
}

public class PublicTokenTest {
    @Test
    void testTokenInit() {
        Token t = new Token("abc.def", 3600);
        assertEquals("abc.def", t.accessToken);
        assertEquals(3600, t.expiresIn);
    }

    @Test
    void testTokenExpiryNegative() {
        Token t = new Token("xyz", -10);
        assertTrue(t.expiresIn < 0);
    }
}