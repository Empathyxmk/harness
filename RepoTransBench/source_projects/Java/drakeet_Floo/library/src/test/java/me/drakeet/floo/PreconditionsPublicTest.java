package me.drakeet.floo;

import org.junit.Test;
import static org.junit.Assert.*;

public class PreconditionsPublicTest {

    @Test
    public void testCheckNotNull_nonNull_public() {
        String s = "not null";
        assertSame(s, Preconditions.checkNotNull(s));
    }

    @Test(expected = NullPointerException.class)
    public void testCheckNotNull_null_public() {
        Preconditions.checkNotNull(null);
    }
}