package com.picklepete.pyicloud.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ConstDriveTest {
    @Test
    public void testConstDriveLoads() {
        try {
            Class<?> clazz = Class.forName("com.picklepete.pyicloud.consts.ConstDrive");
            assertNotNull(clazz);
        } catch (ClassNotFoundException e) {
            fail("ConstDrive class/module not found.");
        }
    }
}