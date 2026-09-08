package com.example.mammoth.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class ResultsModuleTest {
    @Test
    void testSuccessIsSuccessful() {
        Result<String> result = Result.success("foo");
        assertTrue(result.isSuccessful());
        assertEquals("foo", result.getValue());
        assertNull(result.getError());
    }

    @Test
    void testFailureIsNotSuccessful() {
        Result<String> result = Result.failure("Something went wrong");
        assertFalse(result.isSuccessful());
        assertNull(result.getValue());
        assertEquals("Something went wrong", result.getError());
    }

    @Test
    void testMapOnSuccess() {
        Result<Integer> result = Result.success(1);
        Result<Integer> mapped = result.map(x -> x + 1);
        assertTrue(mapped.isSuccessful());
        assertEquals(2, mapped.getValue());
    }

    @Test
    void testMapOnFailure() {
        Result<Integer> result = Result.failure("Error message");
        Result<Integer> mapped = result.map(x -> x + 1);
        assertFalse(mapped.isSuccessful());
        assertEquals("Error message", mapped.getError());
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
        <R> Result<R> map(java.util.function.Function<? super T, ? extends R> func) {
            if (successful) {
                return Result.success(func.apply(value));
            } else {
                return Result.failure(error);
            }
        }
    }
}