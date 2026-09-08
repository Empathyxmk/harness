package com.oxsecurity.maskerlogger.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.oxsecurity.maskerlogger.utils.Utils;

public class TestUtils {

    @Test
    public void testGetConfigFilePath() {
        String path = Utils.getConfigFilePath();
        assertTrue(path.endsWith("gitleaks.toml"));
        assertTrue(path.contains("config"));
    }

    @Test
    public void testGetConfigFilePathCustom() {
        String cfg = Utils.getConfigFilePath("customfile.toml");
        assertTrue(cfg.endsWith("customfile.toml"));
    }
}