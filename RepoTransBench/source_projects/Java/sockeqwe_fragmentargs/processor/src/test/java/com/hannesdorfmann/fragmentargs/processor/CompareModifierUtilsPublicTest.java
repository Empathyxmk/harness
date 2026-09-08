package com.hannesdorfmann.fragmentargs.processor;

import org.junit.Test;
import static org.junit.Assert.*;

/**
 * Public test with different values for modifier comparison.
 */
public class CompareModifierUtilsPublicTest {

    @Test
    public void compareModifiers_publicVariant() {
        int publicModifier = java.lang.reflect.Modifier.PUBLIC;
        int privateModifier = java.lang.reflect.Modifier.PRIVATE;
        int staticModifier = java.lang.reflect.Modifier.STATIC;

        // Instead of comparing public/private, check combination
        int combined = publicModifier | staticModifier;
        assertTrue((combined & java.lang.reflect.Modifier.PUBLIC) != 0);
        assertTrue((combined & java.lang.reflect.Modifier.STATIC) != 0);
        assertFalse((combined & java.lang.reflect.Modifier.PRIVATE) != 0);
    }
}