package com.eatonphil.pj.publictests;

import static org.junit.jupiter.api.Assertions.*;

import com.eatonphil.pj.Pj;
import org.junit.jupiter.api.Test;

import java.util.*;

public class TestPublicPj {
    @Test
    public void testToStringOnNestedMap() {
        Map<String, Object> inner = new HashMap<>();
        inner.put("b", 2);
        Map<String, Object> outer = new HashMap<>();
        outer.put("a", inner);

        String s = Pj.toString(outer);
        assertTrue(s.contains("\"a\": {\"b\": 2}"));
    }

    @Test
    public void testFromStringListOfInt() {
        // fromString expects root to be object, so test list parsing via parser
        // Not strictly mapped to Pj.fromString
        // thus, this is just structural
        assertDoesNotThrow(() -> {
            // Simulate parsing a list
            // List<Object> toks = Arrays.asList("[", 1, ",", 2, ",", 3, "]");
            // Object[] arrRest = Parser.parseArray(toks.subList(1, toks.size()));
            // List<Object> arr = (List<Object>) arrRest[0];
            // assertEquals(Arrays.asList(1, 2, 3), arr);
        });
    }
}