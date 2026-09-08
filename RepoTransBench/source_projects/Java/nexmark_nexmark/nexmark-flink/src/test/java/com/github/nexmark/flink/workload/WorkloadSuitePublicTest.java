package com.github.nexmark.flink.workload;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class WorkloadSuitePublicTest {
    @Test
    void testFromCategoryQueryNamePublic() {
        // Use a different category/query than main test file.
        WorkloadSuite suite = WorkloadSuite.fromCategoryQueryName("cep", "q2");
        assertNotNull(suite);
        assertFalse(suite.suite().isEmpty());
        assertEquals("q2", suite.suite().get(0).queryName);
        assertEquals("cep", suite.suite().get(0).category);
    }

    @Test
    void testFromCategoryQueryNameAllPublic() {
        WorkloadSuite suite = WorkloadSuite.fromCategoryQueryName("oa", "all");
        assertNotNull(suite);
        assertTrue(suite.suite().size() > 5); // Different limit check, must be >5 not just >0
    }
}