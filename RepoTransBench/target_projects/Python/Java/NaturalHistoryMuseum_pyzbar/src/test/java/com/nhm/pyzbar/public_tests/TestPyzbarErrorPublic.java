package com.nhm.pyzbar.public_tests;

import com.nhm.pyzbar.pyzbar_error.PyZbarError;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class TestPyzbarErrorPublic {
    @Test
    void testErrorMessage() {
        PyZbarError e = new PyZbarError("Public test: barcode problem");
        assertEquals("Public test: barcode problem", e.getMessage());
    }

    @Test
    void testErrorRaiseAndCatch() {
        try {
            throw new PyZbarError("Test error for catching");
        } catch (PyZbarError e) {
            assertTrue(e.getMessage().contains("catching"));
        }
    }
}