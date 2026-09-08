package com.github.nexmark.flink;

import org.apache.commons.cli.ParseException;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class BenchmarkTest {

    @Test
    void testMainWithNoArgsThrowsRuntimeException() {
        Exception ex = assertThrows(RuntimeException.class, () -> {
            Benchmark.main(new String[]{});
        });
        assertTrue(ex.getMessage().contains("Usage"));
    }
}