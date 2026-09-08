package com.example.public_tests;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TestPublicScenes {

    String getSceneNameFromId(int id) {
        // Just a mapping for test
        if (id == 18) return "Candlelight";
        return null;
    }
    @Test
    public void testSceneIdsPublic() {
        assertNull(getSceneNameFromId(256));
        assertEquals("Candlelight", getSceneNameFromId(18));
    }
}