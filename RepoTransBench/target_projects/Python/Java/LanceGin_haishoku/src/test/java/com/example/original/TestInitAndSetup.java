package com.example.original;

import org.junit.jupiter.api.Test;
import java.io.File;
import static org.junit.jupiter.api.Assertions.*;

public class TestInitAndSetup {
    @Test
    public void testVersion() {
        String version = com.example.haishoku.Version.getVersion();
        assertNotNull(version);
        assertTrue(version.contains("."));
    }

    @Test
    public void testSetupCallable() {
        File setupPy = new File(System.getProperty("user.dir"), "setup.py");
        assertTrue(setupPy.exists());
    }

    @Test
    public void testLicenseFile() {
        File licenseFile = new File(System.getProperty("user.dir"), "LICENSE");
        assertTrue(licenseFile.exists());
    }
}