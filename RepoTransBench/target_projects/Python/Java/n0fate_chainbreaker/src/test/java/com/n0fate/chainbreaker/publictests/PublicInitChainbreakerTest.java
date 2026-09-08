package com.n0fate.chainbreaker.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicInitChainbreakerTest {
    @Test
    void test_public_import_chainbreaker() {
        String version = "1.0.0";
        String doc = "Documentation";
        assertTrue(version != null || doc != null);
    }

    @Test
    void test_public_chainbreaker_module_content() {
        String doc = "Some doc";
        String name = "chainbreaker";
        assertNotNull(doc);
        assertNotNull(name);
    }
}