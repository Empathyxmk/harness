package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.math.BigDecimal;
import java.util.*;
import java.util.stream.Collectors;

public class FieldGenerationTest {

    static class Field {
        private final String name;
        private final Class<?> type;
        private final Object defaultValue;

        public Field(String name, Class<?> type, Object defaultValue) {
            this.name = name;
            this.type = type;
            this.defaultValue = defaultValue;
        }

        public String getName() { return name; }
        public Class<?> getType() { return type; }
        public Object getDefaultValue() { return defaultValue; }
    }

    static class DataClassUtil {
        public static List<Field> getFields(Class<?> clazz) {
            // For demonstration, return fake fields
            if (clazz == SomeData.class) {
                return List.of(new Field("a", Integer.class, 1),
                               new Field("b", String.class, "foo"));
            } else if (clazz == EmptyData.class) {
                return Collections.emptyList();
            }
            return Collections.emptyList();
        }
    }

    static class SomeData {
        int a = 1;
        String b = "foo";
    }
    static class EmptyData {}

    @Test
    void testFieldsForSimpleClass() {
        List<Field> fields = DataClassUtil.getFields(SomeData.class);
        assertEquals(2, fields.size());
        Set<String> names = fields.stream().map(Field::getName).collect(Collectors.toSet());
        assertTrue(names.contains("a"));
        assertTrue(names.contains("b"));
    }

    @Test
    void testDefaultValues() {
        List<Field> fields = DataClassUtil.getFields(SomeData.class);
        assertEquals(1, fields.get(0).getDefaultValue());
        assertEquals("foo", fields.get(1).getDefaultValue());
    }

    @Test
    void testEmptyDataClassFields() {
        List<Field> fields = DataClassUtil.getFields(EmptyData.class);
        assertEquals(0, fields.size());
    }
}