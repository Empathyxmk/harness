package com.facebook.sparts.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class CompatExtraTest {
    @Test
    public void testStrIsStr() {
        assertTrue("A STRING" instanceof String);
        assertEquals(String.class, "".getClass());
    }

    @Test
    public void testIntIsInt() {
        int x = 12345;
        assertEquals(int.class, ((Object)x).getClass());
    }

    @Test
    public void testUnicodeIsStrPy3() {
        String a = "value";
        assertEquals(String.class, a.getClass());
    }

    @Test
    public void testPy3Features() {
        assertTrue("str".getClass().getDeclaredMethods().length > 0);
        assertNotEquals(java.util.ArrayList.class, java.util.Arrays.asList(2, 3, 4, 5).getClass());
    }

    @Test
    public void testBytesTypes() {
        byte[] arr = "string".getBytes();
        assertTrue(arr instanceof byte[]);
        String s = "xyz";
        assertTrue(s instanceof String);
    }

    @Test
    public void testStringTypesStr() {
        String s = "anotherthing";
        assertTrue(s instanceof String);
    }
}