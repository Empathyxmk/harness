package com.zqqqqz2000.shshsh.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.io.File;

class CwdTest {
    @Test
    void testCurrentWorkingDirectory() {
        String cwd = System.getProperty("user.dir");
        assertNotNull(cwd);
        File dir = new File(cwd);
        assertTrue(dir.exists());
        assertTrue(dir.isDirectory());
    }

    @Test
    void testParentDirectory() {
        String cwd = System.getProperty("user.dir");
        File dir = new File(cwd);
        File parent = dir.getParentFile();
        assertNotNull(parent);
        assertTrue(parent.exists());
        assertTrue(parent.isDirectory());
    }
}