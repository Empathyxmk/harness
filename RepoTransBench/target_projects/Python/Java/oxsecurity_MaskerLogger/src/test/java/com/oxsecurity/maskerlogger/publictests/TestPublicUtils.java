package com.oxsecurity.maskerlogger.publictests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import com.oxsecurity.maskerlogger.utils.Utils;

public class TestPublicUtils {

    @Test
    public void testGetConfigFilePathNonDefault() {
        String path = Utils.getConfigFilePath("alternative_config.toml");
        assertTrue(path.endsWith("alternative_config.toml"));
    }

    @Test
    public void testGetConfigFilePathContainsMaskerlogger() {
        String path = Utils.getConfigFilePath();
        assertTrue(path.contains("maskerlogger"));
    }
}