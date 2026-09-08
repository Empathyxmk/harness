package com.example.public_tests;

import com.example.jsonfield.forms.JSONFormField;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

import java.util.Map;
import java.util.List;

public class PublicFormsTest {

    @Test
    public void testBlankForm() throws Exception {
        // Simulate required=False & blank POST
        JSONFormField field = new JSONFormField(false);
        Object cleaned = field.clean(null);
        assertNull(cleaned);
    }

    @Test
    public void testValidJsonFormValue() throws Exception {
        JSONFormField field = new JSONFormField(false);
        Object cleaned = field.clean("{\"species\": \"cat\", \"legs\": 4}");
        assertTrue(cleaned instanceof Map);
        Map<String, Object> cd = (Map<String, Object>) cleaned;
        assertEquals("cat", cd.get("species"));
        assertEquals(4, ((Number)cd.get("legs")).intValue());
    }

    @Test
    public void testInvalidJsonFormValue() {
        JSONFormField field = new JSONFormField(false);
        Exception e = assertThrows(Exception.class,
                () -> field.clean("{\"species\": unquoted}"));
        assertEquals("Enter valid JSON.", e.getMessage());
    }

    @Test
    public void testPythonObjInput() throws Exception {
        JSONFormField field = new JSONFormField(false);
        Map<String, Object> dict = Map.of("key", List.of(1, 2));
        Object cleaned = field.clean(dict);
        assertTrue(cleaned instanceof Map);
        Map<String, Object> cd = (Map<String, Object>) cleaned;
        assertEquals(List.of(1,2), cd.get("key"));
    }
}