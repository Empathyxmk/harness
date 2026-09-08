package com.example.public_tests;

import com.example.json2html.Json2HtmlStatic;
import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class PublicJson2HtmlAdditionalTest {

    @Test
    void testDeepNesting() {
        Map<String, Object> inner3 = new LinkedHashMap<>();
        inner3.put("x", Arrays.asList("a", "b"));
        Map<String, Object> inner2 = new LinkedHashMap<>();
        inner2.put("y", inner3);
        Map<String, Object> input = new LinkedHashMap<>();
        input.put("z", inner2);

        String output = Json2HtmlStatic.convert(input);
        assertTrue(output.contains("z"));
        assertTrue(output.contains("y"));
        assertTrue(output.contains("x"));
        assertTrue(output.contains("a"));
        assertTrue(output.contains("b"));
    }

    @Test
    void testListOfDictsHeaders() {
        List<Map<String, Object>> input = new ArrayList<>();
        Map<String, Object> m1 = new LinkedHashMap<>();
        m1.put("head", "val1");
        Map<String, Object> m2 = new LinkedHashMap<>();
        m2.put("head", "val2");
        input.add(m1);
        input.add(m2);

        String output = Json2HtmlStatic.convert(input);
        assertTrue(output.contains("head"));
        assertTrue(output.contains("val1"));
        assertTrue(output.contains("val2"));
    }
}