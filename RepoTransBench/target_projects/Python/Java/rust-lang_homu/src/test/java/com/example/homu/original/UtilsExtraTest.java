package com.example.homu.original;

import com.example.homu.utils.Utils;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.HashMap;
import java.util.Map;

public class UtilsExtraTest {

    @Test
    public void testMergeDicts() {
        Map<String, Integer> d1 = new HashMap<>();
        d1.put("a", 1); d1.put("b", 2);
        Map<String, Integer> d2 = new HashMap<>();
        d2.put("b", 3); d2.put("c", 4);
        Map<String, Integer> d = Utils.mergeDicts(d1, d2);
        assertEquals((Integer)1, d.get("a"));
        assertEquals((Integer)3, d.get("b"));
        assertEquals((Integer)4, d.get("c"));
    }

    @Test
    public void testStripDefault() {
        assertEquals("dog:foo", Utils.stripDefault(":user:dog:foo", "user:"));
        assertEquals(":dog", Utils.stripDefault(":dog", ":cat"));
    }

    @Test
    public void testLazyDebugPrints() {
        String val = Utils.lazyDebug("message", 42, 99);
        assertNotNull(val);
        assertTrue(val.contains("message"));
    }
}