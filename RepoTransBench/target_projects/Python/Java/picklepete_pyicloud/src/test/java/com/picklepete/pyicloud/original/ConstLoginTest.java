package com.picklepete.pyicloud.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ConstLoginTest {
    @Test
    public void testConstLoginLoads() {
        try {
            Class<?> clazz = Class.forName("com.picklepete.pyicloud.consts.ConstLogin");
            assertNotNull(clazz);
        } catch (ClassNotFoundException e) {
            fail("ConstLogin class/module not found.");
        }
    }
}