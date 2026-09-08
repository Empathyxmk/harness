package com.xworkflows.original;

import com.xworkflows.compat.CompatUtils;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestCompat {

    @Test
    public void testImportCompatDirectSrc() {
        assertEquals("abc", CompatUtils.u("abc"));
        assertTrue(CompatUtils.isString("test"));
        assertFalse(CompatUtils.isString(123));
        assertFalse(CompatUtils.isString(null));
    }

    @Test
    public void testPython2ModeEquivalence() {
        assertTrue(CompatUtils.isString("hey"));
        assertFalse(CompatUtils.isString(new byte[] {1, 2, 3}));
    }

    @Test
    public void testImportCompatFromSrcDirect() {
        // Simulate import using direct reference in Java
        assertEquals("def", CompatUtils.u("def"));
        assertTrue(CompatUtils.isString("abc"));
        assertFalse(CompatUtils.isString(new Object[0]));
    }
}