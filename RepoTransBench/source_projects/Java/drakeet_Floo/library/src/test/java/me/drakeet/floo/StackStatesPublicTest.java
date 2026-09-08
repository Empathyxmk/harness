package me.drakeet.floo;

import org.junit.Test;
import static org.junit.Assert.*;

public class StackStatesPublicTest {

    @Test
    public void testStateValues_public() {
        assertNotEquals(StackStates.ACTIVE, StackStates.PAUSED);
        assertNotEquals(StackStates.PAUSED, StackStates.DESTROYED);
    }

    @Test
    public void testStateEquality_public() {
        assertEquals("ACTIVE", StackStates.ACTIVE);
        assertNotEquals("PAUSED", StackStates.ACTIVE);
    }
}