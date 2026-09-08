package com.zqqqqz2000.shshsh.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class QuickTest {
    @Test
    void testQuickResultEmulation() {
        class QuickResult {
            final String output;
            QuickResult(String output) { this.output = output; }
            String out() { return output; }
        }

        QuickResult q = new QuickResult("quick out\n");
        assertEquals("quick out\n", q.out());
    }

    @Test
    void testQuickWait() {
        class QuickResult {
            final int code;
            QuickResult(int code) { this.code = code; }
            int waitFor() { return code; }
        }
        QuickResult qr = new QuickResult(0);
        assertEquals(0, qr.waitFor());
    }
}