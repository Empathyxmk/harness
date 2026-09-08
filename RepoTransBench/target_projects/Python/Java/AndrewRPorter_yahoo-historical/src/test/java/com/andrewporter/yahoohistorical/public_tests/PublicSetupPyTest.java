package com.andrewporter.yahoohistorical.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

/**
 * Java translation of public_tests/test_public_setup_py.py.
 * Verifies public characteristics of the setup.py file.
 */
public class PublicSetupPyTest {

    /**
     * This public test should verify (in a "public" fashion) that setup.py
     * contains the basic metadata fields and is importable.
     * Here we mimic basic field presence since we cannot really run setup.py.
     */
    @Test
    public void testPublicSetupPyMetadataFields() throws IOException {
        String content = Files.readString(Paths.get("setup.py"));
        assertNotNull(content, "setup.py should be readable");
        String[] keys = {
            "author",
            "name",
            "url",
            "version",
            "packages",
            "install_requires"
        };
        for (String key : keys) {
            assertTrue(content.contains(key), "setup.py should contain field: " + key);
        }
    }
}