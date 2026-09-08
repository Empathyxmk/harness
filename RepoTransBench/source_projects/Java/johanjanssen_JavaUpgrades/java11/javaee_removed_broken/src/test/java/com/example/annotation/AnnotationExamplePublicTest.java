package com.example.annotation;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class AnnotationExamplePublicTest {
    @Test
    void testAnnotationMessagePublic() {
        AnnotationExample example = new AnnotationExample();
        // Use different test data/assertions if possible
        assertTrue(example.isAnnotated());
    }
}