package org.jak_linux.dns66;

import org.junit.Test;
import static org.junit.Assert.*;

public class ExamplePublicUnitTest {
    @Test
    public void addition_isCorrect_public() {
        assertEquals(7, 3 + 4); // 3+4 instead of 2+2
    }

    @Test
    public void string_equality_public() {
        assertEquals("dns66", "dn" + "s66"); // different from ExampleUnitTest
    }
}