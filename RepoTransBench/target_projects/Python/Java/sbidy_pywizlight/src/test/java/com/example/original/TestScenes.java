package com.example.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TestScenes {

    // Dummy scenes logic
    static int getIdFromSceneName(String name) {
        if ("Alarm".equals(name)) return 35;
        else throw new IllegalArgumentException("Unknown scene name");
    }

    @Test
    public void testGetIdFromSceneNameThrows() {
        assertThrows(IllegalArgumentException.class, () -> getIdFromSceneName("non_exist"));
    }

    @Test
    public void testGetIdFromSceneNameAlarm() {
        assertEquals(35, getIdFromSceneName("Alarm"));
    }
}