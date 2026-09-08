package com.thomasa88.public_tests;

import com.thomasa88.ParamSpec;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

public class PublicParserTest {

    @Test
    void testParamSpecNameValue() {
        ParamSpec spec = new ParamSpec("public_name", "17");
        assertEquals("public_name", spec.var);
        assertEquals("17", spec.member);
    }

    @Test
    void testParamSpecStrAndEq() {
        ParamSpec spec1 = new ParamSpec("ab", "9");
        ParamSpec spec2 = new ParamSpec("ab", "9");
        ParamSpec spec3 = new ParamSpec("ab", "8");
        String s = "(" + spec1.var + ", " + spec1.member + ")";
        assertEquals(s, "(" + spec1.var + ", " + spec1.member + ")");
        assertEquals(spec1, spec2);
        assertNotEquals(spec1, spec3);
    }
}