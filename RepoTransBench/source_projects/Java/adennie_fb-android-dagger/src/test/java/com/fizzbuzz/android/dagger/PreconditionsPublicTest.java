package com.fizzbuzz.android.dagger;

import org.junit.Test;

public class PreconditionsPublicTest {

    @Test
    public void testCheckNotNullNotNullPublic() {
        // Use a different object than original
        String myString = "notNullPublic";
        Preconditions.checkNotNull(myString, "Must not be null");
        Preconditions.checkNotNull(myString);
        Integer myInt = 5;
        Preconditions.checkNotNull(myInt);
    }

    @Test(expected = NullPointerException.class)
    public void testCheckNotNullNullPublic() {
        Preconditions.checkNotNull(null, "Error: is null");
    }

    @Test
    public void testCheckStateTruePublic() {
        Preconditions.checkState(2 > 1, "True expected");
        Preconditions.checkState(true);
    }

    @Test(expected = IllegalStateException.class)
    public void testCheckStateFalsePublic() {
        Preconditions.checkState(3 < 1, "Should fail");
    }
}