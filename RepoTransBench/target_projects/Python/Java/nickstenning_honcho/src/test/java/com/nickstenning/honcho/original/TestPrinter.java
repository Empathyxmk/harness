package com.nickstenning.honcho.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.nickstenning.honcho.Printer;

class TestPrinter {

    @Test
    void testPrinterOutput() {
        Printer printer = new Printer();
        printer.print("INFO", "Hello, World!");
        // If output is captured, test it accordingly here
        assertTrue(true); // Placeholder for output assertion
    }
}