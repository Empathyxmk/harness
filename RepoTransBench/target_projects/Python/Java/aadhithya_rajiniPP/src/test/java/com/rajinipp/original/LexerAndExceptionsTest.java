package com.rajinipp.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class LexerAndExceptionsTest {

    @Test
    void testLexerAddAndGetTokens() throws Exception {
        // Basic tokens: just a couple for smoke test
        java.util.Map<String, String> tokens = new java.util.HashMap<>();
        tokens.put("NUM", "\\d+");
        tokens.put("PLUS", "\\+");
        com.rajinipp.lexer.Lexer lexer = new com.rajinipp.lexer.Lexer(tokens);
        Object lexObj = lexer.getLexer();
        // Should have a method named "lex"
        assertNotNull(lexObj.getClass().getMethod("lex", String.class));
        java.util.List<?> result = new java.util.ArrayList<>();
        try {
            java.lang.reflect.Method lexMethod = lexObj.getClass().getMethod("lex", String.class);
            Object tokensObj = lexMethod.invoke(lexObj, "3 + 5");
            java.util.List<Object> tokensList = new java.util.ArrayList<>();
            for (Object t : (Iterable<?>) tokensObj) {
                tokensList.add(t);
            }
            java.util.Set<String> names = new java.util.HashSet<>();
            for (Object t : tokensList) {
                names.add((String) t.getClass().getField("name").get(t));
            }
            assertEquals(new java.util.HashSet<>(java.util.Arrays.asList("NUM", "PLUS")), names);
        } catch (Exception e) {
            fail("Lexer lex failed: " + e.getMessage());
        }
    }

    @Test
    void testLexerIgnoreCommentsAndWhitespace() throws Exception {
        java.util.Map<String, String> tokens = new java.util.HashMap<>();
        tokens.put("ID", "[a-zA-Z_]+");
        tokens.put("EQ", "=");
        com.rajinipp.lexer.Lexer lexer = new com.rajinipp.lexer.Lexer(tokens);
        Object lexObj = lexer.getLexer();
        String code = "foo = bar   !! this is a comment\nbaz=qux";
        java.util.List<Object> tokensList = new java.util.ArrayList<>();
        try {
            java.lang.reflect.Method lexMethod = lexObj.getClass().getMethod("lex", String.class);
            Object resultObj = lexMethod.invoke(lexObj, code);
            for (Object t : (Iterable<?>) resultObj) {
                tokensList.add(t);
            }
        } catch (Exception e) {
            fail("Lexer lex failed: " + e.getMessage());
        }
        java.util.List<String> names = new java.util.ArrayList<>();
        for (Object t : tokensList) {
            try {
                names.add((String) t.getClass().getField("name").get(t));
            } catch (Exception ex) {
                fail(ex.toString());
            }
        }
        assertEquals(java.util.Arrays.asList("ID", "EQ", "ID", "ID", "EQ", "ID"), names);
    }

    @Test
    void testBreakException() {
        // Simulate: with pytest.raises(exceptions.BreakException)
        Exception exception = assertThrows(com.rajinipp.exceptions.BreakException.class, () -> {
            throw new com.rajinipp.exceptions.BreakException("Break now");
        });
        assertTrue(exception.getMessage().contains("Break now"));
    }

    @Test
    void testReturnExceptionValue() {
        String msg = "Return!";
        int retVal = 42;
        com.rajinipp.exceptions.ReturnException exception = assertThrows(
                com.rajinipp.exceptions.ReturnException.class,
                () -> {
                    throw new com.rajinipp.exceptions.ReturnException(msg, retVal);
                });
        assertEquals(retVal, exception.returnValue);
        assertTrue(exception.getMessage().contains(msg));
    }
}