package com.cloudconvert.publictests;

import org.junit.jupiter.api.Test;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;

class PublicUtilsTest {

    @Test
    void testToCamelCase() {
        assertEquals("fooBar", toCamelCase("foo_bar"));
    }
    @Test
    void testSnakeCase() {
        assertEquals("foo_bar", toSnakeCase("fooBar"));
    }
    private static String toCamelCase(String s) {
        String[] parts = s.split("_");
        if (parts.length == 0) return s;
        String res = parts[0];
        for (int i = 1; i < parts.length; ++i) {
            res += parts[i].substring(0, 1).toUpperCase() + parts[i].substring(1);
        }
        return res;
    }
    private static String toSnakeCase(String s) {
        return s.replaceAll("([A-Z])", "_$1").toLowerCase().replaceAll("^_", "");
    }
}