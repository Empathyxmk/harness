package com.eatonphil.pj.publictests;

import static org.junit.jupiter.api.Assertions.*;

import com.eatonphil.pj.lexer.Lexer;
import org.junit.jupiter.api.Test;

import java.util.*;

public class TestPublicLexer {
    @Test
    public void testLexEscaped() {
        Object[] escaped1 = Lexer.lexEscaped("\"foo\\\"bar\"");
        assertEquals("foo\\", escaped1[0].toString().substring(0, 4));
        assertTrue(escaped1[1] instanceof String);
    }

    @Test
    public void testNextLexedNumber() {
        Object[] result = Lexer.nextLexed("1234 more text");
        assertEquals(1234, result[0]);
        assertTrue(((String)result[1]).contains("more"));
    }
}