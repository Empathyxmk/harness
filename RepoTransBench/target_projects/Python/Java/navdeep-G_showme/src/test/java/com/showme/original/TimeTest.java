package com.showme.original;

import com.showme.Showme;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

class TimeTest {
    @Test
    void testShowmeTimeDecorator() {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        PrintStream oldOut = System.out;
        System.setOut(new PrintStream(out));
        try {
            int result = Showme.time(() -> {
                for (int i = 0; i < 1000; ++i) {
                    double a = Math.pow(i, i);
                }
                return 1;
            });
            String output = out.toString();
            assertTrue(output.contains("Execution speed of"));
            assertTrue(output.contains("ms"));
            assertEquals(1, result);
        } finally {
            System.setOut(oldOut);
        }
    }
}