package com.example.original;

import com.example.jsonfield.forms.JSONFormField;
import org.junit.jupiter.api.Test;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

public class TestFormsTest {

    @Test
    public void testBlankForm() throws Exception {
        JSONFormField field = new JSONFormField(false);
        Object cleaned = field.clean("");
        assertNull(cleaned);
    }

    @Test
    public void testFormWithData() throws Exception {
        JSONFormField field = new JSONFormField(false);
        Object cleaned = field.clean("{}");
        assertTrue(cleaned instanceof Map);
    }

    @Test
    public void testSaveValues() throws Exception {
        Object[][] values = {
                {"object", "{\"a\": \"b\"}", Map.of("a", "b")},
                {"array", "[1, 2]", java.util.List.of(1, 2)},
                {"string", "\"test\"", "test"},
                {"float", "1.2", 1.2},
                {"int", "1234", 1234},
                {"bool", "true", true},
                {"null", "null", null}
        };

        for (Object[] val : values) {
            String input = (String) val[1];
            Object expected = val[2];
            JSONFormField field = new JSONFormField(false);
            Object cleaned = field.clean(input);
            if (expected instanceof Double) {
                assertEquals((Double) expected, ((Number) cleaned).doubleValue(), 1e-8);
            } else if (expected instanceof Integer) {
                assertEquals(((Integer) expected).intValue(), ((Number) cleaned).intValue());
            } else {
                assertEquals(expected, cleaned);
            }
        }
    }

    @Test
    public void testInvalidValue() {
        JSONFormField field = new JSONFormField(false);
        Exception exc = assertThrows(Exception.class, () -> field.clean("foo"));
        assertEquals("Enter valid JSON.", exc.getMessage());
    }
}