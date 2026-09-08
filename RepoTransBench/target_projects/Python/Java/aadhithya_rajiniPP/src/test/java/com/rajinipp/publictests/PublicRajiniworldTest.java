package com.rajinipp.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicRajiniworldTest {

    @Test
    void testPublicVarsAndFunctionsDictNonempty() {
        try {
            Class<?> clazz = Class.forName("rajinipp.__rajiniworld__");
            Object vars = clazz.getDeclaredField("__vars__").get(null);
            Object funcs = clazz.getDeclaredField("__functions__").get(null);
            assertTrue(vars instanceof java.util.Map, "__vars__ should be a Map");
            assertTrue(funcs instanceof java.util.Map, "__functions__ should be a Map");
            assertNotNull(vars);
            assertNotNull(funcs);
        } catch (Exception e) {
            fail("Module or fields missing: " + e.toString());
        }
    }
}