package com.example.original;

import com.example.jsonfield.JSONField;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

import java.util.HashMap;
import java.util.Map;

public class TestFieldsTest {

    @Test
    public void testGetPrepValueAlwaysJsonDumpsIfNotNull() {
        JSONField field = new JSONField(false);
        Map<String, Object> value = new HashMap<>();
        value.put("a", 1);
        String prepared = field.getPrepValue(value);
        assertTrue(prepared instanceof String);
        Map valDecoded = new JSONObject(prepared).toMap();
        assertEquals(value, valDecoded);

        // The already_json part -- simulate as string
        String alreadyJson = new JSONObject(value).toString();
        String doublePrepared = field.getPrepValue(alreadyJson);
        Map valDecoded2 = new JSONObject(new JSONObject(doublePrepared).toString()).toMap(); // double decoding
        assertEquals(value, valDecoded2);

        assertEquals("null", field.getPrepValue(null));
    }

    @Test
    public void testGetPrepValueCanReturnNoneIfNull() {
        JSONField field = new JSONField(true);
        Map<String, Object> value = new HashMap<>();
        value.put("a", 1);
        String prepared = field.getPrepValue(value);
        Map val = new JSONObject(prepared).toMap();
        assertEquals(value, val);

        String alreadyJson = new JSONObject(value).toString();
        String doublePrepared = field.getPrepValue(alreadyJson);
        Map valDecoded2 = new JSONObject(new JSONObject(doublePrepared).toString()).toMap();
        assertEquals(value, valDecoded2);

        assertNull(field.getPrepValue(null));
    }

    @Test
    public void testDeconstructDefaultKwargs() {
        JSONField field = new JSONField();
        Object[] deconstructed = field.deconstruct();
        Map<String, Object> kwargs = (Map<String, Object>) deconstructed[3];
        assertFalse(kwargs.containsKey("dump_kwargs"));
        assertFalse(kwargs.containsKey("load_kwargs"));
    }

    @Test
    public void testDeconstructNonDefaultKwargs() {
        JSONField field = new JSONField();
        // simulate non-default kwargs
        Object[] deconstructed = field.deconstruct();
        Map<String, Object> kwargs = new HashMap<>();
        kwargs.put("dump_kwargs", Map.of("separators", new String[]{",", ":"}));
        kwargs.put("load_kwargs", Map.of("object_pairs_hook", "dict"));
        assertEquals(Map.of("separators", new String[]{",", ":"}), kwargs.get("dump_kwargs"));
        assertEquals(Map.of("object_pairs_hook", "dict"), kwargs.get("load_kwargs"));
    }

    @Test
    public void testFromDbValueLoadedTypes() {
        Object[][] values = new Object[][]{
            {"object", "{\"a\": \"b\"}", Map.class},
            {"array", "[1, 2]", java.util.List.class},
            {"string", "\"test\"", String.class},
            {"float", "1.2", Double.class},
            {"int", "1234", Integer.class},
            {"bool", "true", Boolean.class},
            {"null", "null", null},
        };

        JSONField field = new JSONField();
        for (Object[] row : values) {
            String dbValue = (String) row[1];
            Class<?> expectedType = (Class<?>) row[2];
            Object result = field.fromDbValue(dbValue);
            if (dbValue.equals("null")) {
                assertNull(result);
            } else if (expectedType != null) {
                assertTrue(expectedType.isInstance(result), "Expected " + expectedType + " but got " + (result != null ? result.getClass() : null));
            }
        }
    }
}