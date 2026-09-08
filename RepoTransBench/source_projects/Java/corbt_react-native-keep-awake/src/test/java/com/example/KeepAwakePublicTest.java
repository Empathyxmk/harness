package com.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Public tests for the KeepAwake class.
 * These tests follow the same logic and functionality as the private/internal tests,
 * but use different test data or sequence variations to ensure coverage with new scenarios.
 */
class KeepAwakePublicTest {

    @Test
    void testNotAwakeAfterConstruction() {
        KeepAwake ka = new KeepAwake();
        // Check initial state remains sleeping and not awake
        assertEquals(false, ka.isAwake());
        assertNotEquals("Awake", ka.getStatus());
        assertEquals("Sleeping", ka.getStatus());
    }

    @Test
    void testActivateFromFalse() {
        KeepAwake ka = new KeepAwake();
        // Activate once, should be awake
        ka.activate();
        assertEquals(true, ka.isAwake());
        // Confirm getStatus gives "Awake"
        assertTrue(ka.getStatus().contains("Awake"));
    }

    @Test
    void testDeactivateAfterActivation() {
        KeepAwake ka = new KeepAwake();
        ka.setAwake(true); // Activate using setAwake
        ka.deactivate();
        // Should now be sleeping
        assertFalse(ka.isAwake());
        assertFalse(ka.getStatus().equals("Awake"));
    }

    @Test
    void testMultipleActivatesRemainAwake() {
        KeepAwake ka = new KeepAwake();
        // Activate multiple times
        ka.activate();
        ka.activate();
        ka.activate();
        assertTrue(ka.isAwake());
        assertEquals("Awake", ka.getStatus());
    }

    @Test
    void testMultipleDeactivatesRemainSleeping() {
        KeepAwake ka = new KeepAwake();
        ka.deactivate();
        ka.deactivate();
        assertFalse(ka.isAwake());
        assertEquals("Sleeping", ka.getStatus());
    }

    @Test
    void testSetAwakeToTrueSetsAwakeStatus() {
        KeepAwake ka = new KeepAwake();
        ka.setAwake(true);
        assertEquals(true, ka.isAwake());
        assertEquals("Awake", ka.getStatus());
    }

    @Test
    void testSetAwakeToFalseFromAwake() {
        KeepAwake ka = new KeepAwake();
        ka.activate();
        ka.setAwake(false);
        assertEquals(false, ka.isAwake());
        assertEquals("Sleeping", ka.getStatus());
    }

    @Test
    void testToggleMultipleTimes() {
        KeepAwake ka = new KeepAwake();
        ka.activate();
        assertEquals("Awake", ka.getStatus());
        ka.deactivate();
        assertEquals("Sleeping", ka.getStatus());
        ka.activate();
        assertEquals("Awake", ka.getStatus());
        ka.deactivate();
        assertEquals("Sleeping", ka.getStatus());
    }
}