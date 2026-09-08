package com.trentb.public_tests;

import com.trentb.iterstrat.MlStratifiers;
import org.junit.jupiter.api.Test;

import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.*;

class TestPublicInitAndSetup {
    @Test
    void testPublicReadmeExists() {
        Path readmePath = Path.of(System.getProperty("user.dir"), "README.md");
        assertTrue(Files.exists(readmePath), "README.md must exist in project root");
    }

    @Test
    void testPublicLicenseExists() {
        Path licensePath = Path.of(System.getProperty("user.dir"), "LICENSE");
        assertTrue(Files.exists(licensePath), "LICENSE must exist in project root");
    }

    @Test
    void testPublicImportIterstrat() {
        assertDoesNotThrow(() -> Class.forName("com.trentb.iterstrat.IterativeStratification"));
    }

    @Test
    void testPublicImportMlStratifiers() {
        // Public test: check for MultilabelStratifiedShuffleSplit
        assertDoesNotThrow(() -> {
            Class<?> shuffle = Class.forName("com.trentb.iterstrat.MlStratifiers$MultilabelStratifiedShuffleSplit");
            assertNotNull(shuffle);
        });
    }
}