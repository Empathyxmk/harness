package com.example.public_tests;

import com.example.jsonfield.JSONField;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

import java.util.Map;

public class PublicFieldsTest {
    @Test
    public void testDeconstructNonDefaultKwargs() {
        JSONField f = new JSONField();
        Object[] deconstructed = f.deconstruct();
        Map<String, Object> kwargs = java.util.Map.of(
                "encoder_class", String.class,
                "decoder_class", String.class,
                "dump_kwargs", Map.of("indent", 4)
        );
        assertEquals(String.class, kwargs.get("encoder_class"));
        assertEquals(String.class, kwargs.get("decoder_class"));
        assertEquals(Map.of("indent", 4), kwargs.get("dump_kwargs"));
    }

    @Test
    public void testDeconstructDefaultKwargs() {
        JSONField f = new JSONField();
        Object[] deconstructed = f.deconstruct();
        Map<String, Object> kwargs = (Map<String, Object>) deconstructed[3];
        assertFalse(kwargs.containsKey("decoder_class"));
        assertFalse(kwargs.containsKey("encoder_class"));
        assertFalse(kwargs.containsKey("dump_kwargs"));
    }

    @Test
    public void testGetPrepValueCanReturnNoneIfNull() {
        JSONField field = new JSONField(true);
        assertNull(field.getPrepValue(null));
    }

    @Test
    public void testGetPrepValueAlwaysJsonDumpsIfNotNull() {
        JSONField field = new JSONField(true);
        java.util.Map<String, Object> value = java.util.Map.of("number", 33, "flag", false);
        String val = field.getPrepValue(value);
        assertEquals("{\"number\":33,\"flag\":false}", val.replace(" ", ""));
    }

    @Test
    public void testFromDbValueLoadedTypes() {
        JSONField field = new JSONField();
        Object o1 = field.fromDbValue("{\"z\":1}");
        assertTrue(o1 instanceof Map && ((Map)o1).get("z").equals(1));
        assertNull(field.fromDbValue(null));
    }
}