package com.example.original;

import com.example.json2html.Json2HtmlStatic;
import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class Json2HtmlAdditionalTest {

    @Test
    void testEmptyList() {
        List<Object> input = new ArrayList<>();
        String result = Json2HtmlStatic.convert(input);
        assertTrue(result.contains("<ul>") && result.contains("</ul>"));
    }

    @Test
    void testNullInput() {
        String result = Json2HtmlStatic.convert(null);
        assertNotNull(result);
        assertTrue(result.isEmpty() || result.equals("null") || !result.contains("Exception"));
    }

    @Test
    void testListOfMixedTypes() {
        List<Object> input = Arrays.asList("str", 42, true, null);
        String result = Json2HtmlStatic.convert(input);
        assertTrue(result.contains("str"));
        assertTrue(result.contains("42") || result.contains("<li>42</li>"));
        assertTrue(result.contains("true") || result.contains("<li>true</li>"));
        assertTrue(result.toLowerCase().contains("null"));
    }

    @Test
    void testXssInjection() {
        Map<String, Object> input = new LinkedHashMap<>();
        String attackerStr = "<script>alert('hi')</script>";
        input.put("username", "foo");
        input.put("comment", attackerStr);
        String result = Json2HtmlStatic.convert(input);
        // Ensure the output properly escapes html or does not echo executable script
        assertFalse(result.contains(attackerStr));
        assertFalse(result.contains("<script>"));
    }
}