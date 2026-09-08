package com.example.original;

import com.example.json2html.Json2HtmlStatic;
import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class Json2HtmlCoreTest {

    @Test
    void testEmptyDict() {
        Map<String, Object> input = new LinkedHashMap<>();
        String result = Json2HtmlStatic.convert(input);
        assertTrue(result.contains("<table"));
        assertTrue(result.contains("</table>"));
    }

    @Test
    void testBasicMapping() {
        Map<String, Object> input = new LinkedHashMap<>();
        input.put("x", 1);
        input.put("y", 42);
        String result = Json2HtmlStatic.convert(input);
        assertTrue(result.contains("<th>x</th>"));
        assertTrue(result.contains("<td>1</td>"));
        assertTrue(result.contains("<th>y</th>"));
        assertTrue(result.contains("<td>42</td>"));
    }

    @Test
    void testListOfPrimitives() {
        List<String> input = Arrays.asList("a", "b", "c");
        String result = Json2HtmlStatic.convert(input);
        assertTrue(result.contains("<ul>"));
        assertTrue(result.contains("<li>a</li>"));
        assertTrue(result.contains("<li>b</li>"));
        assertTrue(result.contains("<li>c</li>"));
    }

    @Test
    void testNestedDict() {
        Map<String, Object> level2 = new LinkedHashMap<>();
        level2.put("deep", 99);
        Map<String, Object> input = new LinkedHashMap<>();
        input.put("foo", "bar");
        input.put("nested", level2);
        String result = Json2HtmlStatic.convert(input);
        assertTrue(result.contains("nested"));
        assertTrue(result.contains("deep"));
        assertTrue(result.contains("99"));
    }

    @Test
    void testArrayOfDictsClubbing() {
        List<Map<String, Object>> arr = new ArrayList<>();
        Map<String, Object> m1 = new LinkedHashMap<>();
        m1.put("a", 1);
        m1.put("b", 2);
        Map<String, Object> m2 = new LinkedHashMap<>();
        m2.put("a", 3);
        m2.put("b", 4);
        arr.add(m1);
        arr.add(m2);

        String result = Json2HtmlStatic.convert(arr);
        assertTrue(result.contains("<table"));
        assertTrue(result.contains("<th>a</th>") && result.contains("<th>b</th>"));
        assertTrue(result.contains("<td>1</td>") && result.contains("<td>2</td>"));
        assertTrue(result.contains("<td>3</td>") && result.contains("<td>4</td>"));
    }
}