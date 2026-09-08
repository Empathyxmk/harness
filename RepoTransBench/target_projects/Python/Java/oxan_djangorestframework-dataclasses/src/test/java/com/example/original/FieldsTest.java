package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

public class FieldsTest {

    static class Field<T> {
        String name;
        T value;
        public Field(String name, T value) {
            this.name = name; this.value = value;
        }
    }

    @Test
    void testStringFieldNotNull() {
        Field<String> field = new Field<>("foo", "abc");
        assertNotNull(field.value);
    }

    @Test
    void testIntFieldValue() {
        Field<Integer> field = new Field<>("foo", 42);
        assertEquals(42, field.value);
    }

    @Test
    void testDefaultValue() {
        Field<String> field = new Field<>("foo", null);
        assertNull(field.value);
    }
}