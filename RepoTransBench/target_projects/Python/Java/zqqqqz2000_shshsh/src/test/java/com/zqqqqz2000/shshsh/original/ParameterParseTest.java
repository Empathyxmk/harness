package com.zqqqqz2000.shshsh.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class ParameterParseTest {
    // Simulates parsing --flag --key value args as a basic example
    private Map<String, String> parse(String[] args) {
        Map<String, String> res = new HashMap<>();
        for (int i = 0; i < args.length; ++i) {
            String arg = args[i];
            if (arg.startsWith("--")) {
                if ((i + 1) < args.length && !args[i + 1].startsWith("--")) {
                    res.put(arg.substring(2), args[++i]);
                } else {
                    res.put(arg.substring(2), "true");
                }
            }
        }
        return res;
    }

    @Test
    void testFlagParameter() {
        String[] cmd = {"--run"};
        Map<String, String> result = parse(cmd);
        assertTrue(result.containsKey("run"));
        assertEquals("true", result.get("run"));
    }

    @Test
    void testKeyValueParameter() {
        String[] cmd = {"--file", "output.txt"};
        Map<String, String> result = parse(cmd);
        assertTrue(result.containsKey("file"));
        assertEquals("output.txt", result.get("file"));
    }

    @Test
    void testMultipleParameters() {
        String[] cmd = {"--first", "1", "--second", "2", "--flag"};
        Map<String, String> result = parse(cmd);
        assertEquals("1", result.get("first"));
        assertEquals("2", result.get("second"));
        assertEquals("true", result.get("flag"));
    }
}