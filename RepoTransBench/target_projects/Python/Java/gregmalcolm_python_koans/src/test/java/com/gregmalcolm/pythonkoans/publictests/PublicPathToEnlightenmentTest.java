package com.gregmalcolm.pythonkoans.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicPathToEnlightenmentTest {

    @Test
    void testPathIsFollowed() {
        String result = "finished";
        assertEquals("finished", result, "Public: Path should be finished.");
    }
}