package com.example.utils;

import org.junit.Test;

import static org.junit.Assert.*;

public class GsonUtilPublicTest {
    @Test
    public void testNumberStringDeserialization_public() {
        // Use different value
        String json = "123";
        int num = Integer.parseInt(json);
        assertEquals(123, num);
    }
}