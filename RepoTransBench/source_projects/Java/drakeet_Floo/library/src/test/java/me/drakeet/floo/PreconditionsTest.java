package me.drakeet.floo;

import org.junit.Test;

public class PreconditionsTest {

    @Test(expected = NullPointerException.class)
    public void testCheckNotNullThrows() {
        Preconditions.checkNotNull(null, "err");
    }

    @Test
    public void testCheckNotNullNoThrow() {
        Preconditions.checkNotNull("a", "err");
    }

    @Test(expected = IllegalArgumentException.class)
    public void testCheckArgumentThrows() {
        Preconditions.checkArgument(false, "arg error");
    }

    @Test
    public void testCheckArgumentNoThrow() {
        Preconditions.checkArgument(true, "ok arg");
    }
}