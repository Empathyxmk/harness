package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import java.lang.reflect.*;

public class TypingUtilsTest {

    static <T> boolean isCollection(Class<T> clazz) {
        return Collection.class.isAssignableFrom(clazz);
    }

    static <T> boolean isMap(Class<T> clazz) {
        return Map.class.isAssignableFrom(clazz);
    }

    @Test
    void testCollectionTypeDetection() {
        assertTrue(isCollection(List.class));
        assertFalse(isCollection(String.class));
    }

    @Test
    void testMapTypeDetection() {
        assertTrue(isMap(HashMap.class));
        assertFalse(isMap(String.class));
    }

    @Test
    void testOptionalTypeDetection() {
        assertFalse(isCollection(Optional.class));
    }
}