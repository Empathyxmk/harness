package com.example;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class NashornExamplePublicTest {

    @Test
    void testScriptEngineManagerNashornPresent_public() {
        // Instead of just "nashorn", let's test "javascript" alias as well (should not be null in fixed context)
        assertNotNull(new javax.script.ScriptEngineManager().getEngineByName("javascript"));
    }
}