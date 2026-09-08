package com.rajinipp.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicLexerAndExceptionsTest {

    @Test
    void testPublicLexerTokenizationForIdentifier() {
        Object tokens = com.rajinipp.utils.YamlUtils.readYml("rajinipp/token.yml");
        com.rajinipp.lexer.Lexer lexer = new com.rajinipp.lexer.Lexer(tokens);
        Object lexObj = lexer.getLexer();
        java.util.List<Object> result = new java.util.ArrayList<>();
        try {
            java.lang.reflect.Method lexMethod = lexObj.getClass().getMethod("lex", String.class);
            Object tokensObj = lexMethod.invoke(lexObj, "varX1 = 9");
            for (Object t : (Iterable<?>) tokensObj) {
                result.add(t);
            }
        } catch (Exception e) {
            fail("Lexer lex failed: " + e.getMessage());
        }
        boolean hasID = false;
        for (Object t : result) {
            try {
                String name = (String) t.getClass().getField("name").get(t);
                if ("ID".equals(name)) {
                    hasID = true;
                    break;
                }
            } catch (Exception ex) {
                fail(ex.toString());
            }
        }
        assertTrue(hasID, "Should include an identifier");
    }

    @Test
    void testPublicLexerIgnoresComments() {
        Object tokens = com.rajinipp.utils.YamlUtils.readYml("rajinipp/token.yml");
        com.rajinipp.lexer.Lexer lexer = new com.rajinipp.lexer.Lexer(tokens);
        Object lexObj = lexer.getLexer();
        String code = "num = 2  !! this is a comment\nprint num";
        java.util.List<Object> result = new java.util.ArrayList<>();
        try {
            java.lang.reflect.Method lexMethod = lexObj.getClass().getMethod("lex", String.class);
            Object tokensObj = lexMethod.invoke(lexObj, code);
            for (Object t : (Iterable<?>) tokensObj) {
                result.add(t);
            }
        } catch (Exception e) {
            fail("Lexer lex failed: " + e.getMessage());
        }
        StringBuilder codeFragment = new StringBuilder();
        for (Object t : result) {
            try {
                Object val = null;
                try {
                    val = t.getClass().getField("value").get(t);
                } catch (NoSuchFieldException ignored) {}
                if (val != null) { codeFragment.append(val.toString()).append(" "); }
            } catch (Exception ex) {
                // skip
            }
        }
        assertFalse(codeFragment.toString().contains("!!"), "Comments should be ignored");
    }

    @Test
    void testPublicLexerRaiseFileException() {
        // Simulate: monkeypatching read_yml to throw FileNotFoundException.
        // In Java, we simulate by calling with an invalid path
        try {
            com.rajinipp.utils.YamlUtils.readYml("/some/definitely_missing_file_foobar_baz_yml");
            fail("Exception not raised for missing file");
        } catch (Exception e) {
            assertTrue(e instanceof java.io.FileNotFoundException);
        }
    }
}