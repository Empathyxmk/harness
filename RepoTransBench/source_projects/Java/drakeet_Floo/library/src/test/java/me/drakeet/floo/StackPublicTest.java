package me.drakeet.floo;

import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;
import java.util.Arrays;

public class StackPublicTest {

    private Stack<Integer> stack;

    @Before
    public void setUp() {
        stack = new Stack<>();
    }

    @Test
    public void testPushThenPop_public() {
        stack.push(99);
        stack.push(42);
        assertEquals(Integer.valueOf(42), stack.pop());
        assertEquals(Integer.valueOf(99), stack.pop());
    }

    @Test
    public void testIsEmpty_public() {
        assertTrue(stack.isEmpty());
        stack.push(1);
        assertFalse(stack.isEmpty());
    }
}