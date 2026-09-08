package com.nhm.pyzbar.public_tests;

import com.nhm.pyzbar.wrapper.Wrapper;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class TestWrapperPublic {
    @Test
    void testGetSymbolName() {
        String name = Wrapper.getSymbolName(13);
        assertTrue(name.contains("PDF417"));
    }

    @Test
    void testGetSymbolNameInvalid() {
        String name = Wrapper.getSymbolName(1000);
        assertEquals("UNKNOWN", name);
    }
}