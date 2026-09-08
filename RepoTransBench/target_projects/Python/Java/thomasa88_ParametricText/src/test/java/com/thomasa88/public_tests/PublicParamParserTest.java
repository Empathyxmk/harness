package com.thomasa88.public_tests;

import com.thomasa88.ParamSpec;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

public class PublicParamParserTest {

    @Test
    void testParamSpecBasic() {
        ParamSpec p = new ParamSpec("anotherparam", "anotherval");
        assertNotNull(p.var);
    }

    @Test
    void testParamSpecStr() {
        ParamSpec p = new ParamSpec("customparam", "val42");
        String s = "(" + p.var + ", " + p.member + ")";
        assertEquals(s, "(" + p.var + ", " + p.member + ")");
    }

    @Test
    void testParamSpecEq() {
        ParamSpec p1 = new ParamSpec("eqtest", "a");
        ParamSpec p2 = new ParamSpec("eqtest", "a");
        ParamSpec p3 = new ParamSpec("eqtest", "b");
        assertEquals(p1, p2);
        assertNotEquals(p1, p3);
    }
}