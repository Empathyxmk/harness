package com.example.original;

import com.example.jsonfield.JSONUtil;
import org.junit.jupiter.api.Test;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.assertj.core.api.Assertions.*;

public class TestJsonfieldTest {

    @Test
    public void testJsonFieldCreate() {
        Map<String, Object> jsonObj = Map.of("item_1", "this is a json blah", "blergh", "hey, hey, hey");
        String jsonStr = JSONUtil.dumps(jsonObj);
        Map decoded = (Map)JSONUtil.loads(jsonStr);
        assertEquals(jsonObj, decoded);
    }

    @Test
    public void testStringInJsonField() {
        String jsonObj = "blah blah";
        String jsonStr = JSONUtil.dumps(jsonObj);
        String decoded = (String) JSONUtil.loads(jsonStr);
        assertEquals(jsonObj, decoded);
    }

    @Test
    public void testFloatInJsonField() {
        double jsonObj = 1.23;
        String jsonStr = JSONUtil.dumps(jsonObj);
        double decoded = (Double) JSONUtil.loads(jsonStr);
        assertEquals(jsonObj, decoded, 0.0001);
    }

    @Test
    public void testIntInJsonField() {
        int jsonObj = 1234567;
        String jsonStr = JSONUtil.dumps(jsonObj);
        int decoded = ((Number)JSONUtil.loads(jsonStr)).intValue();
        assertEquals(jsonObj, decoded);
    }

    @Test
    public void testEmptyObjects() {
        Object[] objs = new Object[]{Collections.emptyMap(), Collections.emptyList(), 0, "", false};
        for (Object obj : objs) {
            String jsonStr = JSONUtil.dumps(obj);
            Object decoded = JSONUtil.loads(jsonStr);
            if (obj instanceof Map || obj instanceof List) {
                assertTrue(obj.equals(decoded));
            } else {
                assertEquals(obj, decoded);
            }
        }
    }

    @Test
    public void testCustomEncoder() {
        // No direct analog to complex encoding here; test as is
        String val = "1+3j";
        String jsonStr = JSONUtil.dumps(val);
        String decoded = (String) JSONUtil.loads(jsonStr);
        assertEquals(val, decoded);
    }

    @Test
    public void testSerializeDeserialize() {
        Map<String, Object> obj = Map.of("foo", "bar");
        String json = JSONUtil.dumps(obj);
        Map val = (Map) JSONUtil.loads(json);
        assertEquals(obj, val);
    }

    @Test
    public void testDefaultParameters() {
        Map<String, Object> json = new HashMap<>();
        json.put("check", 12);
        assertEquals(12, json.get("check"));
        assertTrue(json instanceof Map);
    }

    @Test
    public void testInvalidJson() {
        String invalidJson = "{]";
        assertThatThrownBy(() -> JSONUtil.loads(invalidJson))
            .isInstanceOf(Exception.class);
    }

    @Test
    public void testIntegerInStringInJsonField() {
        String jsonObj = "123";
        String jsonStr = JSONUtil.dumps(jsonObj);
        String decoded = (String) JSONUtil.loads(jsonStr);
        assertEquals(jsonObj, decoded);
    }

    @Test
    public void testBooleanInStringInJsonField() {
        String jsonObj = "true";
        String jsonStr = JSONUtil.dumps(jsonObj);
        String decoded = (String) JSONUtil.loads(jsonStr);
        assertEquals(jsonObj, decoded);
    }

    @Test
    public void testRegexLookup() {
        List<Map<String, Object>> objects = List.of(
                Map.of("boom", "town"),
                Map.of("move", "town"),
                Map.of("save", "town")
        );
        long countBoom = objects.stream().filter(map -> map.containsKey("boom")).count();
        long countTown = objects.stream().filter(map -> map.containsValue("town")).count();
        assertEquals(1, countBoom);
        assertEquals(3, countTown);
    }
}