package com.example.public_tests;

import com.example.json2html.Json2HtmlStatic;
import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class PublicJson2HtmlCoreTest {

    @Test
    void testBasicTypes() {
        Map<String, Object> input = new LinkedHashMap<>();
        input.put("n", 1);
        input.put("s", "hello");
        input.put("b", true);
        input.put("none", null);
        String output = Json2HtmlStatic.convert(input);
        assertTrue(output.contains("hello"));
        assertTrue(output.contains("1") || output.contains("<td>1</td>"));
        assertTrue(output.toLowerCase().contains("true"));
        assertTrue(output.toLowerCase().contains("null"));
    }

    @Test
    void testListUnordered() {
        List<Object> input = Arrays.asList("a", "b", "c", null, 2);
        String output = Json2HtmlStatic.convert(input);
        assertTrue(output.contains("<ul>"));
        assertTrue(output.contains("<li>a</li>"));
        assertTrue(output.contains("<li>c</li>"));
        assertTrue(output.contains("<li>2</li>"));
        assertTrue(output.toLowerCase().contains("null"));
    }

    @Test
    void testNestedTable() {
        Map<String, Object> inner = Map.of("k", "v");
        Map<String, Object> input = new LinkedHashMap<>();
        input.put("outer", inner);
        String result = Json2HtmlStatic.convert(input);
        assertTrue(result.contains("outer"));
        assertTrue(result.contains("k"));
        assertTrue(result.contains("v"));
    }
}