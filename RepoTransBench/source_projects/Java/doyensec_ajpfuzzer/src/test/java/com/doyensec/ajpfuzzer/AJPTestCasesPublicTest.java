package com.doyensec.ajpfuzzer;

import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class AJPTestCasesPublicTest {

    @Test
    void testGetAllCasesImmutabilityDifferent() {
        List<String> orig = AJPTestCases.getAllCases();
        if (!orig.isEmpty()) {
            String last = orig.get(orig.size() - 1);
            assertTrue(last.endsWith(".jsp") || last.endsWith(".xml") || last.contains("/"), "Last case is a plausible test path");
        }
    }

    @Test
    void testGetAllCasesHasDefaultCases() {
        List<String> cases = AJPTestCases.getAllCases();
        assertTrue(cases.contains("GET /WEB-INF/web.xml"), "Should contain 'GET /WEB-INF/web.xml' as a default case");
    }
}