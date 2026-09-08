package com.zqqqqz2000.shshsh.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class PublicParameterParseTest {
    Map<String, String> parseArgs(String[] args) {
        Map<String, String> result = new HashMap<>();
        for (String arg : args) {
            String[] kv = arg.split("=", 2);
            if (kv.length == 2) {
                result.put(kv[0], kv[1]);
            }
        }
        return result;
    }

    @Test
    void testSingleParameter() {
        Map<String, String> parsed = parseArgs(new String[] {"foo=3"});
        assertEquals(1, parsed.size());
        assertEquals("3", parsed.get("foo"));
    }

    @Test
    void testMultipleParameters() {
        Map<String, String> parsed = parseArgs(new String[] {"a=1", "b=2", "c=hello"});
        assertEquals(3, parsed.size());
        assertEquals("1", parsed.get("a"));
        assertEquals("2", parsed.get("b"));
        assertEquals("hello", parsed.get("c"));
    }

    @Test
    void testNoParameters() {
        Map<String, String> parsed = parseArgs(new String[] {});
        assertTrue(parsed.isEmpty());
    }

    @Test
    void testNonKeyValueIgnored() {
        Map<String, String> parsed = parseArgs(new String[] {"abc", "d=e"});
        assertEquals(1, parsed.size());
        assertEquals("e", parsed.get("d"));
    }
}