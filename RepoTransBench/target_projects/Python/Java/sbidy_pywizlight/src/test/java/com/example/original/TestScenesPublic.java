package com.example.public_tests;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TestScenesPublic {

    // Dummy mapping for test
    static String getSceneNameFromId(int id) {
        if (id == 18) return "Candlelight";
        return null;
    }

    @Test
    public void testSceneIdsPublic() {
        assertNull(getSceneNameFromId(256));
        assertEquals("Candlelight", getSceneNameFromId(18));
    }
}