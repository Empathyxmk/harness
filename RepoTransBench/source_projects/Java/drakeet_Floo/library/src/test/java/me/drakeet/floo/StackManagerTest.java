package me.drakeet.floo;

import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;

public class StackManagerTest {

    private StackManager stackManager;

    @Before
    public void setup() {
        stackManager = new StackManager();
    }

    @Test
    public void testPushAndPeek() {
        Stack stack = new Stack();
        stackManager.push(stack);

        assertSame(stack, stackManager.peek());
    }

    @Test
    public void testPopAndEmpty() {
        Stack stack = new Stack();
        stackManager.push(stack);
        Stack popped = stackManager.pop();
        assertSame(stack, popped);
        assertNull(stackManager.peek());
    }

    @Test
    public void testEmptyPop() {
        assertNull(stackManager.pop());
    }

    @Test
    public void testIsNotEmpty() {
        assertFalse(stackManager.isNotEmpty());
        stackManager.push(new Stack());
        assertTrue(stackManager.isNotEmpty());
    }
}