package com.picklepete.pyicloud.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// For const_account_family.py

public class ConstAccountFamilyTest {
    @Test
    public void testConstAccountFamilyLoads() {
        try {
            Class<?> clazz = Class.forName("com.picklepete.pyicloud.consts.ConstAccountFamily");
            assertNotNull(clazz);
        } catch (ClassNotFoundException e) {
            fail("ConstAccountFamily class/module not found.");
        }
    }
}