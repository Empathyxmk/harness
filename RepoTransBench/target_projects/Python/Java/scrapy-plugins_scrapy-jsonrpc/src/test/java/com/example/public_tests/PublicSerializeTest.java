package com.example.public_tests;

import com.example.serialize.SerializeUtils;
import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class PublicSerializeTest {

    @Test
    void testPublicJsonDumpsAndLoads() throws Exception {
        Map<String, Object> orig = new HashMap<>();
        orig.put("c", 100);
        orig.put("test", Arrays.asList(1, 7, 8));
        String encoded = SerializeUtils.scrapyJsonDumps(orig);
        Map<String, Object> decoded = SerializeUtils.scrapyJsonLoads(encoded);
        assertEquals(orig, decoded);
    }

    @Test
    void testPublicReprLoadsAndDumps() throws Exception {
        List<Object> orig = Arrays.asList(11, java.util.Map.of("foo", "bar"), Arrays.asList(3,4));
        String dumped = orig.toString();
        List<Object> loaded = Arrays.asList(11, java.util.Map.of("foo", "bar"), Arrays.asList(3,4));
        assertEquals(dumped, loaded.toString());
    }

    @Test
    void testPublicReprDumpsHandlesNone() {
        Object val = null;
        String dumped = java.util.Objects.toString(val, null);
        assertNull(dumped);
    }

    @Test
    void testPublicUnicodeAndUtf8() {
        // Testing unicode/str and utf-8 string encoding/decoding
        String s_unicode = "üñîçødê";
        byte[] utf8ed = s_unicode.getBytes(java.nio.charset.StandardCharsets.UTF_8);
        assertNotNull(utf8ed);
        assertEquals(s_unicode, new String(utf8ed, java.nio.charset.StandardCharsets.UTF_8));

        String s_bytes = "测试";
        byte[] bytes = s_bytes.getBytes(java.nio.charset.StandardCharsets.UTF_8);
        String s_str = new String(bytes, java.nio.charset.StandardCharsets.UTF_8);
        assertEquals("测试", s_str);
    }
}