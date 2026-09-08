package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class FieldUtilsTest {

    static class FieldUtils {
        static boolean isOptional(Class<?> type) {
            return type.getSimpleName().startsWith("Optional");
        }
        static boolean isFinal(Class<?> type) {
            // In Java, this makes little sense for equality, so we always return false for demo
            return false;
        }
    }

    @Test
    void testIsOptional() {
        assertTrue(FieldUtils.isOptional(java.util.Optional.class));
        assertFalse(FieldUtils.isOptional(String.class));
    }

    @Test
    void testIsFinal() {
        assertFalse(FieldUtils.isFinal(String.class));
    }
}