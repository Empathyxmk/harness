package com.eatonphil.pj.original;

import static org.junit.jupiter.api.Assertions.*;

import com.eatonphil.pj.lexer.Lexer;
import org.junit.jupiter.api.Test;

import java.util.*;

public class TestLexer {
    @Test
    public void testLexString() throws Exception {
        Object[] result = Lexer.lexString("\"foobar\"");
        assertEquals("foobar", result[0]);
        assertEquals("", result[1]);
    }

    @Test
    public void testLexStringWithRemainder() throws Exception {
        Object[] result2 = Lexer.lexString("\"foo\"x");
        assertEquals("foo", result2[0]);
        assertEquals("x", result2[1]);
    }

    @Test
    public void testLexNumber() {
        Object[] result = Lexer.lexNumber("123 ");
        assertEquals(123, result[0]);
        assertTrue(result[1].toString().startsWith(" "));

        Object[] result2 = Lexer.lexNumber("-10.2,");
        assertEquals(-10.2, (Double)result2[0], 0.0001);
        assertTrue(result2[1].toString().startsWith(","));
    }

    @Test
    public void testLexBool() {
        Object[] trueRes = Lexer.lexBool("true, x");
        assertEquals(true, trueRes[0]);
        assertTrue(trueRes[1].toString().startsWith(","));

        Object[] falseRes = Lexer.lexBool("false }");
        assertEquals(false, falseRes[0]);
        assertTrue(falseRes[1].toString().startsWith("}"));
    }

    @Test
    public void testLexNull() {
        Object[] nullRes = Lexer.lexNull("null,");
        assertNull(nullRes[0]);
        assertTrue(nullRes[1].toString().startsWith(","));
    }

    @Test
    public void testLexSimple() {
        List<Object> toks = Lexer.lex("{\"foo\": 1, \"bar\": 2}");
        assertEquals("[{, foo, :, 1, ,, bar, :, 2, }]", toks.toString().replace("\"", ""));
    }
}