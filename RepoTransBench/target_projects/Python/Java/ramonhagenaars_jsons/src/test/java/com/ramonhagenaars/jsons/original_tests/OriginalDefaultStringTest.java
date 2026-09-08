package com.ramonhagenaars.jsons.original_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class OriginalDefaultStringTest {

    @Test
    void testStringEquals() {
        String s = "foobar";
        assertEquals("foobar", s);
    }

    @Test
    void testStringConcat() {
        String s = "foo" + "bar";
        assertEquals("foobar", s);
    }
}