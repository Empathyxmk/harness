package com.facebook.sparts.public_;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class PublicCompatExtraTest {
    @Test
    public void testPublicStrIsStr() {
        assertTrue("a" instanceof String);
        assertEquals(String.class, "".getClass());
    }
    
    @Test
    public void testPublicIntIsInt() {
        int y = 42;
        assertEquals(int.class, ((Object)y).getClass());
    }

    @Test
    public void testPublicUnicodeIsStrPy3() {
        String z = "foo";
        assertEquals(String.class, z.getClass());
    }

    @Test
    public void testPublicPy3Features() {
        assertTrue("".getClass().getDeclaredMethods().length > 0); // Has 'format'
        assertNotEquals(java.util.ArrayList.class, java.util.Arrays.asList(1, 2, 3).getClass());
    }

    @Test
    public void testPublicBytesTypes() {
        byte[] a = "abc".getBytes();
        assertTrue(a instanceof byte[]);
        String b = "def";
        assertTrue(b instanceof String);
    }

    @Test
    public void testPublicStringTypesStr() {
        String s = "something";
        assertTrue(s instanceof String);
    }
}