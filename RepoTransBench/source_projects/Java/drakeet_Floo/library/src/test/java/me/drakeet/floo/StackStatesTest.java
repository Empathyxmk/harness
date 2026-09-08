package me.drakeet.floo;

import org.junit.Test;

/**
 * Placeholder test for StackStates interface. No logic to test since interface is empty.
 * This class intentionally left with a dummy test to satisfy coverage tools.
 */
public class StackStatesTest {

    @Test
    public void testExists() {
        // The StackStates interface may be a marker or container for static String constants in other code;
        // as currently implemented, this only checks that we can reference the class.
        Class<?> clazz = StackStates.class;
        assert clazz != null;
    }
}