package com.eatonphil.pj.original;

import static org.junit.jupiter.api.Assertions.*;

import com.eatonphil.pj.parser.Parser;
import com.eatonphil.pj.lexer.Lexer;
import org.junit.jupiter.api.Test;

import java.util.*;

public class TestParser {

    @Test
    public void testParseArray() {
        List<Object> toks = new ArrayList<>();
        toks.add("1");
        toks.add(",");
        toks.add("2");
        toks.add(",");
        toks.add("3");
        toks.add("]");
        Object[] res = Parser.parseArray(toks);
        List<Object> arr = (List<Object>) res[0];

        assertEquals(3, arr.size());
        assertEquals("1", arr.get(0));
        assertEquals("2", arr.get(1));
        assertEquals("3", arr.get(2));
    }

    @Test
    public void testParseObject() {
        // input: foo : 1, bar : 2 }
        List<Object> toks = Arrays.asList("foo", ":", 1, ",", "bar", ":", 2, "}");
        Object[] res = Parser.parseObject(toks);
        Map<String, Object> m = (Map<String, Object>) res[0];
        assertEquals(2, m.size());
        assertEquals(1, m.get("foo"));
        assertEquals(2, m.get("bar"));
    }

    @Test
    public void testParseLiteral() {
        List<Object> toks = Arrays.asList(1, ",");
        Object[] res = Parser.parse(toks, false);
        assertEquals(1, res[0]);
        assertEquals(Arrays.asList(","), res[1]);
    }

    @Test
    public void testParseJsonRoot() {
        List<Object> toks = Lexer.lex("{\"x\": 1, \"y\": 2}");
        Object[] res = Parser.parse(toks, true);
        Map<String, Object> m = (Map<String, Object>) res[0];
        assertEquals(2, m.size());
        assertEquals(1, m.get("x"));
        assertEquals(2, m.get("y"));
    }
}