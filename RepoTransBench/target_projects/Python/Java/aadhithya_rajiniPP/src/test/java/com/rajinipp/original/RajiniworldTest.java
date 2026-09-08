package com.rajinipp.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class RajiniworldTest {

    @Test
    void testVarsAndFunctionsAreDicts() {
        try {
            // Simulate importlib.import_module("rajinipp.__rajiniworld__")
            Class<?> clazz = Class.forName("rajinipp.__rajiniworld__");
            Object vars = clazz.getDeclaredField("__vars__").get(null);
            Object funcs = clazz.getDeclaredField("__functions__").get(null);
            assertTrue(vars instanceof java.util.Map, "__vars__ should be a Map");
            assertTrue(funcs instanceof java.util.Map, "__functions__ should be a Map");
        } catch (Exception e) {
            fail("Module or required fields missing: " + e.toString());
        }
    }
}