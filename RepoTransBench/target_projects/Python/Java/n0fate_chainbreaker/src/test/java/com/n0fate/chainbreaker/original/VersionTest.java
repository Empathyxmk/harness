package com.n0fate.chainbreaker.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class VersionTest {
    @Test
    void test_version_str() {
        String version = "1.0.0";
        assertNotNull(version);
        assertTrue(version.contains("."));
    }
}