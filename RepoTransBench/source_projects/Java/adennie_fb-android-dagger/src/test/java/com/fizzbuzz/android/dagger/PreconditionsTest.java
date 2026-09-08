package com.fizzbuzz.android.dagger;

import org.junit.Test;

import static com.fizzbuzz.android.dagger.Preconditions.checkState;
import static org.junit.Assert.fail;

public class PreconditionsTest {

    @Test
    public void testCheckState_TrueCondition() {
        // Should not throw an exception
        checkState(true, "This message should not be seen.");
    }

    @Test(expected = IllegalStateException.class)
    public void testCheckState_FalseCondition() {
        // Should throw IllegalStateException with the provided message
        checkState(false, "This is an error message.");
    }

    @Test
    public void testCheckState_FalseConditionWithMessage() {
        try {
            checkState(false, "Custom error message");
            fail("Expected IllegalStateException not thrown");
        } catch (IllegalStateException e) {
            assertEquals("Custom error message", e.getMessage());
        }
    }
}