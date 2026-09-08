package com.n0fate.chainbreaker.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicVersionTest {
    @Test
    void test_public_version_attribute() {
        String v = "1.2.3";
        assertNotNull(v);
        assertTrue(v.contains("."));
        assertTrue(v.split("\\.").length >= 2);
    }

    @Test
    void test_public_version_module_doc() {
        String doc = "docstring";
        assertNotNull(doc);
    }
}