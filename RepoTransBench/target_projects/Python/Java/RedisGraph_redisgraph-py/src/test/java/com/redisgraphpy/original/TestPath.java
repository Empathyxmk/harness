// Supplemental to cover path.py extra edge cases.
package com.redisgraphpy.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestPath {

    @Test
    void testPathEmpty() {
        Path path = new Path(java.util.List.of(), java.util.List.of());
        assertEquals(0, path.length());
    }
}