package com.asciimoo.drawille.public_tests;

import com.asciimoo.drawille.Canvas;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class PublicSpeedTest {
    @Test
    void testCanvasSpeedPublic() {
        Canvas canvas = new Canvas();
        for (int y = 0; y < 80; y += 2) {
            canvas.set(15, y);
        }
        String buf = canvas.frame();
        // Buffer should not be empty, should contain the braille char
        boolean found = buf.chars().anyMatch(c -> c >= 0x2800);
        assertTrue(found, "Should contain braille char after line set");
        canvas.clear();
        String buf2 = canvas.frame();
        // After clear, there should be no braille chars present
        boolean none = buf2.chars().noneMatch(c -> c >= 0x2800);
        assertTrue(none, "Should be empty after clear");
    }
}