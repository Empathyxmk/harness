package me.drakeet.floo;

import org.junit.Test;

import static org.junit.Assert.*;

public class StackTest {

    @Test
    public void testStatesAndResult() {
        Stack stack = new Stack();
        assertEquals(StackStates.STATE_CREATED, stack.getState());
        stack.setState(StackStates.STATE_INITED);
        assertEquals(StackStates.STATE_INITED, stack.getState());

        stack.setResult("result");
        assertEquals("result", stack.getResult());
    }

    @Test
    public void testStackCallback() {
        Stack stack = new Stack();
        class Callback implements StackCallback {
            boolean called = false;
            @Override
            public void run(Stack s) {
                called = true;
                assertSame(stack, s);
            }
        }
        Callback cb = new Callback();
        stack.setCallback(cb);
        stack.onResult();
        assertTrue(cb.called);
    }
}