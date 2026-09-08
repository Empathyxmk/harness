package com.doyensec.ajpfuzzer;

import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class AJPTestCasesExtraPublicTest {

    @Test
    void testGetAllCasesNonEmpty() {
        List<String> cases = AJPTestCases.getAllCases();
        assertFalse(cases.isEmpty(), "Should not be empty");
    }

    @Test
    void testGetAllCasesContainsTest() {
        List<String> cases = AJPTestCases.getAllCases();
        boolean found = false;
        for (String s : cases) {
            if (s.startsWith("GET ")) {
                found = true;
                break;
            }
        }
        assertTrue(found, "At least one case should start with 'GET '");
    }
}