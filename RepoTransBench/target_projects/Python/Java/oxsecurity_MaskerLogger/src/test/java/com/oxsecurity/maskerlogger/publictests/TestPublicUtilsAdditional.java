package com.oxsecurity.maskerlogger.publictests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import com.oxsecurity.maskerlogger.utils.Utils;

public class TestPublicUtilsAdditional {

    @Test
    public void testGetConfigFilePathOtherCustom() {
        String cfg = Utils.getConfigFilePath("anotherpublic.toml");
        assertTrue(cfg.endsWith("anotherpublic.toml"));
    }

    @Test
    public void testGetConfigFilePathFolderCheck() {
        String cfg = Utils.getConfigFilePath();
        boolean found = false;
        for (String part : cfg.split("/")) {
            if (part.equals("config")) found = true;
        }
        if (!found) {
            for (String part : cfg.split("\\\\")) {
                if (part.equals("config")) found = true;
            }
        }
        assertTrue(found);
    }
}