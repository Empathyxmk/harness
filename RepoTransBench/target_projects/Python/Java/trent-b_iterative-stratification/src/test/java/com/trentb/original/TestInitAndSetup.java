package com.trentb.original;

import com.trentb.iterstrat.MlStratifiers;
import org.junit.jupiter.api.Test;

import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.*;

class TestInitAndSetup {
    @Test
    void testReadmeExists() {
        Path readmePath = Path.of(System.getProperty("user.dir"), "README.md");
        assertTrue(Files.exists(readmePath), "README.md must exist in project root");
    }

    @Test
    void testLicenseExists() {
        Path licensePath = Path.of(System.getProperty("user.dir"), "LICENSE");
        assertTrue(Files.exists(licensePath), "LICENSE must exist in project root");
    }

    @Test
    void testImportIterstrat() {
        // In Java, if code compiles, package is importable.
        assertDoesNotThrow(() -> Class.forName("com.trentb.iterstrat.IterativeStratification"));
    }

    @Test
    void testImportMlStratifiers() {
        // Expect MultilabelStratifiedKFold as nested class in MlStratifiers
        assertDoesNotThrow(() -> {
            Class<?> kfold = Class.forName("com.trentb.iterstrat.MlStratifiers$MultilabelStratifiedKFold");
            assertNotNull(kfold);
        });
    }
}