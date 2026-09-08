package com.zqqqqz2000.shshsh.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.nio.file.Paths;
import java.nio.file.Path;

/**
 * Tests simulating working directory queries and behaviors.
 */
class PublicCwdTest {
    @Test
    void testGetCurrentWorkingDirectory() {
        Path cwd = Paths.get("").toAbsolutePath();
        String systemCwd = System.getProperty("user.dir");
        assertTrue(cwd.toString().equals(systemCwd)
                   || cwd.normalize().toString().equals(Paths.get(systemCwd).normalize().toString()));
    }

    @Test
    void testParentDirectory() {
        Path cwd = Paths.get("").toAbsolutePath();
        Path parent = cwd.getParent();
        assertNotNull(parent);
        assertTrue(cwd.toString().startsWith(parent.toString()));
    }
}