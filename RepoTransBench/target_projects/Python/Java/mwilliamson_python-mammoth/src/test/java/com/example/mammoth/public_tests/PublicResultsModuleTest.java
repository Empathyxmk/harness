package com.example.mammoth.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicResultsModuleTest {
    @Test
    void testPublicSuccessResult() {
        Result<Integer> result = Result.success(42);
        assertTrue(result.isSuccessful());
        assertEquals(42, result.getValue());
    }

    @Test
    void testPublicFailureResult() {
        Result<String> result = Result.failure("Failed publicly");
        assertFalse(result.isSuccessful());
        assertEquals("Failed publicly", result.getError());
    }

    // Helper Result class for demonstration; actual implementation should match source library
    static class Result<T> {
        private final boolean successful;
        private final T value;
        private final String error;
        private Result(boolean successful, T value, String error) {
            this.successful = successful;
            this.value = value;
            this.error = error;
        }
        static <T> Result<T> success(T value) { return new Result<>(true, value, null); }
        static <T> Result<T> failure(String error) { return new Result<>(false, null, error); }
        boolean isSuccessful() { return successful; }
        T getValue() { return value; }
        String getError() { return error; }
    }
}