package com.example;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class NashornExamplePublicTest {

    @Test
    void testScriptEngineManagerAvailable_public() {
        // Instead of "nashorn", we try another engine name like "JavaScript" for public test (should be null in Nashorn broken context)
        assertNull(new javax.script.ScriptEngineManager().getEngineByName("JavaScript"));
    }
}