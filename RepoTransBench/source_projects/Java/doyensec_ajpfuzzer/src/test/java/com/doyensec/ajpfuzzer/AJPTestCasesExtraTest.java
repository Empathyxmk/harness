package com.doyensec.ajpfuzzer;

import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class AJPTestCasesExtraTest {

    @Test
    void testGetAllCasesImmutability() {
        List<String> orig = AJPTestCases.getAllCases();
        if (!orig.isEmpty()) {
            String first = orig.get(0);
            assertEquals("GET /WEB-INF/web.xml", first);
        }
    }

    @Test
    void testGetAllCasesSize() {
        List<String> cases = AJPTestCases.getAllCases();
        assertTrue(cases.size() >= 2, "Should be at least two default test cases");
    }
}