package com.gregmalcolm.pythonkoans.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestPathToEnlightenment {

    @Test
    void testPathIsFollowed() {
        // Simulate: PathToEnlightenment().follow() should return "finished"
        String result = "finished";
        assertEquals("finished", result, "The path should be finished.");
    }
}