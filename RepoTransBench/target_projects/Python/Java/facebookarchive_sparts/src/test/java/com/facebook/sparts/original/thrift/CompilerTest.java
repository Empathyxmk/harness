package com.facebook.sparts.original.thrift;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class CompilerTest {
    @Test
    public void testCompilerSim() {
        String arg = "abc.thrift";
        assertTrue(arg.endsWith(".thrift"));
        assertEquals(9, arg.length());
    }
}