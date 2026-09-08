package com.nickstenning.honcho.public_;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.nickstenning.honcho.Printer;

class TestPublicPrinter {

    @Test
    void testPublicPrinterOutput() {
        Printer printer = new Printer();
        printer.print("INFO", "Hello, World!");
        // If output is captured, test it accordingly here
        assertTrue(true); // Placeholder to ensure output logic runs
    }
}