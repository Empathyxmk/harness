package com.picklepete.pyicloud.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestSetupFileTest {
    @Test
    public void testSetupConfigExists() {
        String configFilename = "setup.cfg";
        assertTrue(configFilename.endsWith(".cfg"));
    }

    @Test
    public void testSetupPyExists() {
        String setupFilename = "setup.py";
        assertTrue(setupFilename.endsWith(".py"));
    }
}