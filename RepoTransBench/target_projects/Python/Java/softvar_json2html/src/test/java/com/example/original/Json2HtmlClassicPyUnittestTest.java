package com.example.original;

import com.example.json2html.Json2HtmlStatic;
import org.junit.jupiter.api.Test;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class Json2HtmlClassicPyUnittestTest {

    @Test
    void testOnlyOneLevel() {
        Map<String, Object> input = new LinkedHashMap<>();
        input.put("foo", 123);
        input.put("bar", "baz");
        String result = Json2HtmlStatic.convert(input);
        assertTrue(result.contains("<th>foo</th>"));
        assertTrue(result.contains("<td>123</td>"));
        assertTrue(result.contains("<th>bar</th>"));
        assertTrue(result.contains("<td>baz</td>"));
    }

    @Test
    void testListAsDictionaryValue() {
        List<Object> l = Arrays.asList(7, 8, 9);
        Map<String, Object> input = new LinkedHashMap<>();
        input.put("nums", l);
        String output = Json2HtmlStatic.convert(input);
        assertTrue(output.contains("<th>nums</th>"));
        assertTrue(output.contains("7"));
        assertTrue(output.contains("8"));
        assertTrue(output.contains("9"));
        assertTrue(output.contains("<ul>"));
    }

    @Test
    void testComplicatedNesting() {
        Map<String, Object> l2 = new LinkedHashMap<>();
        l2.put("key2", Arrays.asList(1, 2));
        Map<String, Object> l1 = new LinkedHashMap<>();
        l1.put("key1", l2);

        Map<String, Object> input = new LinkedHashMap<>();
        input.put("outer", l1);

        String res = Json2HtmlStatic.convert(input);
        assertTrue(res.contains("outer"));
        assertTrue(res.contains("key1"));
        assertTrue(res.contains("key2"));
        assertTrue(res.contains("1"));
        assertTrue(res.contains("2"));
    }
}