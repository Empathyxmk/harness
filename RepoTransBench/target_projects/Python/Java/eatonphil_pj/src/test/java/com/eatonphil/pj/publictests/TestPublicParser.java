package com.eatonphil.pj.publictests;

import static org.junit.jupiter.api.Assertions.*;

import com.eatonphil.pj.parser.Parser;
import org.junit.jupiter.api.Test;

import java.util.*;

public class TestPublicParser {
    @Test
    public void testParseArrayPublic() {
        List<Object> toks = Arrays.asList(1, ",", 2, ",", 3, "]");
        Object[] arrRest = Parser.parseArray(toks);
        List<Object> arr = (List<Object>) arrRest[0];
        assertEquals(3, arr.size());
        assertEquals(1, arr.get(0));
        assertEquals(2, arr.get(1));
    }

    @Test
    public void testParseObjectPublic() {
        List<Object> toks = Arrays.asList("foo", ":", 1, "}");
        Object[] objRest = Parser.parseObject(toks);
        Map<String, Object> obj = (Map<String, Object>) objRest[0];
        assertEquals(1, obj.size());
        assertEquals(1, obj.get("foo"));
    }
}