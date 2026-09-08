package com.example.jsoncsv.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

public class TestPublicEscape {

    private String encodeSafeKey(List<String> path, String sep) {
        List<String> parts = new ArrayList<>();
        for (String segment : path) {
            parts.add(segment.replace("\\", "\\\\").replace(sep, "\\" + sep));
        }
        return String.join("\\" + sep, parts);
    }

    private List<String> decodeSafeKey(String key, String sep) {
        List<String> result = new ArrayList<>();
        StringBuilder curr = new StringBuilder();
        boolean escape = false;
        for (int i = 0; i < key.length(); i++) {
            char c = key.charAt(i);
            if (escape) {
                curr.append(c);
                escape = false;
            } else if (c == '\\') {
                escape = true;
            } else if ((""+c).equals(sep)) {
                result.add(curr.toString());
                curr.setLength(0);
            } else {
                curr.append(c);
            }
        }
        result.add(curr.toString());
        return result;
    }

    @Test
    public void test_public_all() {
        List<String> path = Arrays.asList("A", "B", "..", "\\.\\ww");
        List<String> _path = null;
        for (char sep : "AB.w".toCharArray()) {
            String key = encodeSafeKey(path, String.valueOf(sep));
            _path = decodeSafeKey(key, String.valueOf(sep));
        }
        assertEquals(path, _path);
    }

    @Test
    public void test_public_encode() {
        List<String> path = Arrays.asList("A", "B", "C", "www.xxx.com");
        String sep = ".";
        String key = encodeSafeKey(path, sep);
        assertEquals("A\\.B\\.C\\.www.xxx.com", key);
    }

    @Test
    public void test_public_decode() {
        String key = "A\\.B\\.C\\.www.xxx.com";
        String sep = ".";
        List<String> path = decodeSafeKey(key, sep);
        assertEquals("A", path.get(0));
        assertEquals("B", path.get(1));
        assertEquals("C", path.get(2));
        assertEquals("www.xxx.com", path.get(3));
    }
}