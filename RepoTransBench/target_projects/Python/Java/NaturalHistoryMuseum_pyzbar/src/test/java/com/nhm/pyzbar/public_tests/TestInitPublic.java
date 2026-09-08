package com.nhm.pyzbar.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestInitPublic {
    @Test
    void testInitPublic() {
        try {
            Class<?> pyzbar = Class.forName("com.nhm.pyzbar.Pyzbar");
            assertNotNull(pyzbar.getDeclaredField("__doc__"));
            assertNotNull(pyzbar.getDeclaredField("__version__"));
        } catch (Exception e) {
            fail("pyzbar class must have '__doc__' and '__version__'");
        }
    }
}