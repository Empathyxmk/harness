package com.example.public_tests;

import com.example.jsonfield.json.json;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.Map;
import java.util.List;

public class PublicJsonfieldTest {
    @Test
    public void testPublicEncodeSimpleDict() {
        java.util.Map<String, Object> data = java.util.Map.of("planet", "Saturn", "rings", true);
        String encoded = json.dumps(data);
        assertEquals("{\"planet\":\"Saturn\",\"rings\":true}", encoded.replace(" ", ""));
    }

    @Test
    public void testPublicEncodeListNumbers() {
        List<Integer> data = List.of(5, 7, 11);
        String encoded = json.dumps(data);
        assertEquals("[5,7,11]", encoded.replace(" ", ""));
    }

    @Test
    public void testPublicDecodeUnicode() {
        String inputStr = "{\"emoji\": \"\\u263A\"}";
        Map<String, Object> output = (Map<String, Object>) json.loads(inputStr);
        assertEquals("\u263A", output.get("emoji"));
    }

    @Test
    public void testPublicInvalidJsonRaises() {
        Exception e = assertThrows(Exception.class, () -> json.loads("{invalid: true,}"));
        assertTrue(e.getMessage().contains("Invalid JSON") || e instanceof RuntimeException);
    }

    @Test
    public void testPublicNativeFloatEncoding() {
        double data = 42.42;
        assertEquals("42.42", json.dumps(data));
        Object loaded = json.loads("42.42");
        if (loaded instanceof Number) {
            assertEquals(42.42, ((Number) loaded).doubleValue(), 1e-8);
        } else {
            fail("Decoded value not a number");
        }
    }
}