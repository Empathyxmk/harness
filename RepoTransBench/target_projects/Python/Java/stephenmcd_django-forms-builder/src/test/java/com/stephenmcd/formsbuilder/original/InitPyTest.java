package com.stephenmcd.formsbuilder.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class InitPyTest {

    @Test
    public void testVersionString() {
        String __version__ = "1.2.3";
        assertTrue(__version__ instanceof String);
        assertEquals(2, __version__.chars().filter(ch -> ch == '.').count());
    }
}