package com.picklepete.pyicloud.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ConstFindMyiPhoneTest {
    @Test
    public void testConstFindMyiPhoneLoads() {
        try {
            Class<?> clazz = Class.forName("com.picklepete.pyicloud.consts.ConstFindMyiPhone");
            assertNotNull(clazz);
        } catch (ClassNotFoundException e) {
            fail("ConstFindMyiPhone class/module not found.");
        }
    }
}