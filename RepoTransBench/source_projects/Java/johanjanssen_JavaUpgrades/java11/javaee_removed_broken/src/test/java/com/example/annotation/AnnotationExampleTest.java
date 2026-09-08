package com.example.annotation;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class AnnotationExampleTest {
    @Test
    public void testMainNoExceptions() {
        assertDoesNotThrow(() -> AnnotationExample.main(new String[0]));
    }
}