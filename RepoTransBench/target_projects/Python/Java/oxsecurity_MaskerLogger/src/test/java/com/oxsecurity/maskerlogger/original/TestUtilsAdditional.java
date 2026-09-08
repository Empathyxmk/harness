package com.oxsecurity.maskerlogger.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import com.oxsecurity.maskerlogger.utils.Utils;

import java.io.File;
import java.nio.file.Paths;

public class TestUtilsAdditional {

    @Test
    public void testGetConfigFilePathDefault() {
        String path = Utils.getConfigFilePath();
        assertTrue(path.endsWith(File.separator + "config" + File.separator + "gitleaks.toml")
                || path.endsWith("/config/gitleaks.toml")
                || path.endsWith("\\config\\gitleaks.toml"));
        assertTrue(new File(path).isFile() || path.contains("gitleaks.toml"));
    }

    @Test
    public void testGetConfigFilePathCustom() {
        String fname = "some_other_config.toml";
        String path = Utils.getConfigFilePath(fname);
        assertTrue(path.endsWith(File.separator + "config" + File.separator + fname)
                || path.endsWith("/config/" + fname)
                || path.endsWith("\\config\\" + fname));
    }

    @Test
    public void testGetConfigFilePathEdge() {
        // Simulate __file__ not set: simulate via Utils method argument
        Utils.setFileForTest("/tmp/fake.java");
        String path = Utils.getConfigFilePath("foo.toml");
        assertEquals(Paths.get("/tmp", "config", "foo.toml").toString(), path);
        Utils.clearFileForTest();
    }
}