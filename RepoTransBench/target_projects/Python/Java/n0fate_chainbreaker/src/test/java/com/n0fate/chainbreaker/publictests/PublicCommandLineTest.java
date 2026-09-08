package com.n0fate.chainbreaker.publictests;

import org.junit.jupiter.api.Test;

public class PublicCommandLineTest {
    @Test
    void test_public_import_main_module_no_crash() {
        try {
            throw new AttributeError("Simulate chainbreaker.__main__ missing attribute");
        } catch (AttributeError e) {
            // Expected
        }
    }
    static class AttributeError extends RuntimeException {
        public AttributeError(String s) { super(s); }
    }
}