package com.showme.original;

import com.showme.Showme;

import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import static org.junit.jupiter.api.Assertions.*;

class CpuTimeTest {
    @Test
    void testShowmeCputimeDecorator() {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        PrintStream oldOut = System.out;
        System.setOut(new PrintStream(out));
        try {
            int result = Showme.cputime(() -> {
                for (int i = 0; i < 1000; ++i) {
                    double a = Math.pow(i, i);
                }
                return 1;
            });
            String output = out.toString();
            assertTrue(output.contains("CPU time for"));
            assertEquals(1, result);
        } finally {
            System.setOut(oldOut);
        }
    }
}