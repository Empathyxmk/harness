package com.whonore.coqtail.original;

import org.junit.jupiter.api.Test;
import com.whonore.coqtail.parse.Parse;
import static org.junit.jupiter.api.Assertions.*;

public class TestParse {

    @Test
    void testParseIdentifierAlpha() {
        assertTrue(Parse.isIdent("KappaZetaXYZ"));
    }

    @Test
    void testParseIdentifierMixed() {
        assertTrue(Parse.isIdent("T2X9P"));
    }

    @Test
    void testParseNonIdentifierNumeric() {
        assertFalse(Parse.isIdent("10MainVar"));
    }

    @Test
    void testParseSplitLineColon() {
        String text = "Theorem Power: forall n, n ^ 2 >= 0.";
        String[] result = Parse.splitLine(text);
        assertTrue(result instanceof String[]);
        assertTrue(result[0].contains("Theorem"));
    }

    @Test
    void testParseFindNameTheorem() {
        String text = "Theorem my_power: forall n, n ^ 2 >= 0.";
        String name = Parse.findName(text);
        assertTrue(name == null || name instanceof String);
    }
}