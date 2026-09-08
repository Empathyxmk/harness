package com.eatonphil.pj.original;

import static org.junit.jupiter.api.Assertions.*;

import com.eatonphil.pj.Pj;
import org.junit.jupiter.api.Test;

import java.util.*;

public class TestPj {

    @Test
    public void testToStringListAndMap() {
        List<Object> l = Arrays.asList(1, "foo", true, 2.5, false, null);

        String s = Pj.toString(l);
        // Should be: [1, "foo", true, 2.5, false, None]
        assertTrue(s.contains("[1, \"foo\", true, 2.5, false, None]") ||
            s.replaceAll(" ", "").equals("[1,\"foo\",true,2.5,false,None]"));
    }

    @Test
    public void testFromStringToMap() {
        String s = "{\"a\": 1, \"b\": 2}";
        Map<String, Object> m = Pj.fromString(s);
        assertEquals(2, m.size());
        assertEquals(1, m.get("a"));
        assertEquals(2, m.get("b"));
    }
}