package com.nhm.pyzbar.original;

import com.nhm.pyzbar.pyzbar_error.PyZbarError;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class TestPyzbarError {

    @Test
    void testPyzbarErrorIsException() {
        assertTrue(Exception.class.isAssignableFrom(PyZbarError.class), "PyZbarError must be an Exception");
    }

    @Test
    void testPyzbarErrorRaiseAndStr() {
        PyZbarError e = new PyZbarError("fail");
        Exception thrown = assertThrows(PyZbarError.class, () -> {
            throw e;
        });
        assertEquals("fail", thrown.getMessage());
    }
}