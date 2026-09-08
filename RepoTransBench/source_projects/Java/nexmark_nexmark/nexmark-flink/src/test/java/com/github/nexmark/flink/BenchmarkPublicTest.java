package com.github.nexmark.flink;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class BenchmarkPublicTest {

    @Test
    void testMainWithNullArgsThrowsRuntimeException() {
        Exception ex = assertThrows(RuntimeException.class, () -> {
            Benchmark.main(null);
        });
        // The error message should refer to args/usage, so check similar wording but not identical
        assertTrue(ex.getMessage().toLowerCase().contains("usage"));
    }

    @Test
    void testMainWithInvalidArgsThrowsParseExceptionOrRuntime() {
        Exception ex = assertThrows(Exception.class, () -> {
            Benchmark.main(new String[]{"--foo"});
        });
        // Accepts RuntimeException or ParseException, just check that it's not a pass
        assertNotNull(ex.getMessage());
    }
}