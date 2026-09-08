package com.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class KeepAwakeTest {

    @Test
    void testInitialState() {
        KeepAwake ka = new KeepAwake();
        assertFalse(ka.isAwake());
        assertEquals("Sleeping", ka.getStatus());
    }

    @Test
    void testActivate() {
        KeepAwake ka = new KeepAwake();
        ka.activate();
        assertTrue(ka.isAwake());
        assertEquals("Awake", ka.getStatus());
    }

    @Test
    void testDeactivate() {
        KeepAwake ka = new KeepAwake();
        ka.activate();
        ka.deactivate();
        assertFalse(ka.isAwake());
        assertEquals("Sleeping", ka.getStatus());
    }

    @Test
    void testActivateIdempotence() {
        KeepAwake ka = new KeepAwake();
        ka.activate();
        ka.activate(); // Should remain true
        assertTrue(ka.isAwake());
    }

    @Test
    void testDeactivateIdempotence() {
        KeepAwake ka = new KeepAwake();
        ka.deactivate(); // Still false
        assertFalse(ka.isAwake());
    }

    @Test
    void testSetAwakeTrue() {
        KeepAwake ka = new KeepAwake();
        ka.setAwake(true);
        assertTrue(ka.isAwake());
    }

    @Test
    void testSetAwakeFalse() {
        KeepAwake ka = new KeepAwake();
        ka.setAwake(true);
        ka.setAwake(false);
        assertFalse(ka.isAwake());
    }

    @Test
    void testMultipleTransitions() {
        KeepAwake ka = new KeepAwake();
        ka.setAwake(true);
        assertEquals("Awake", ka.getStatus());
        ka.setAwake(false);
        assertEquals("Sleeping", ka.getStatus());
        ka.setAwake(true);
        assertEquals("Awake", ka.getStatus());
    }
}