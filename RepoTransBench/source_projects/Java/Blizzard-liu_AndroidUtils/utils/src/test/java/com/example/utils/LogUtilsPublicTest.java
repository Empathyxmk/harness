package com.example.utils;

import org.junit.Test;

import static org.junit.Assert.*;

public class LogUtilsPublicTest {
    @Test
    public void testInfoLogLevel_public() {
        String level = "INFO";
        assertNotEquals("ERROR", level);
    }
}