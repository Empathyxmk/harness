package com.github.tonyo.pyope.original;

import com.github.tonyo.pyope.util.Util;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;

class UtilsTest {

    @Test
    void testBitStringConversion() {
        assertArrayEquals(new int[]{}, Util.strToBitstring(new byte[]{}));
        assertArrayEquals(new int[]{0, 1, 0, 0, 0, 0, 0, 1}, Util.strToBitstring("A".getBytes()));
        assertArrayEquals(
            new int[]{0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0},
            Util.strToBitstring("AB".getBytes())
        );
    }
}