package com.github.davidmoten.geo.util;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

public class PreconditionsPublicTest {

    @Test
    public void testCheckArgumentThrowsWithDifferentData() {
        Exception ex = assertThrows(IllegalArgumentException.class, () -> {
            Preconditions.checkArgument(2 + 2 == 5, "Math doesn't work!");
        });
        assertTrue(ex.getMessage().contains("Math doesn't work!"));
    }

    @Test
    public void testCheckNotNullThrowsWithDifferentData() {
        Exception ex = assertThrows(NullPointerException.class, () -> {
            Preconditions.checkNotNull(null, "Object must not be null!");
        });
        assertTrue(ex.getMessage().contains("Object must not be null!"));
    }
}