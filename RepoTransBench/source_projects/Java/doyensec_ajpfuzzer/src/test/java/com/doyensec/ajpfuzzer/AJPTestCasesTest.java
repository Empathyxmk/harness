package com.doyensec.ajpfuzzer;

import org.junit.jupiter.api.Test;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class AJPTestCasesTest {

    @Test
    void testGetAllCasesReturnsNonEmptyList() {
        List<String> cases = AJPTestCases.getAllCases();
        assertNotNull(cases);
        assertFalse(cases.isEmpty());
    }

    @Test
    void testCaseContainsKnownAttackPayloads() {
        List<String> cases = AJPTestCases.getAllCases();
        String found = cases.stream().filter(s -> s.contains("/WEB-INF/web.xml")).findAny().orElse(null);
        assertNotNull(found);
    }

    @Test
    void testListIsUnmodifiable() {
        List<String> c1 = AJPTestCases.getAllCases();
        assertThrows(UnsupportedOperationException.class, () -> c1.add("test-case"));
    }
}