package com.hannesdorfmann.fragmentargs.processor;

import org.junit.Test;
import static org.junit.Assert.*;

/**
 * Public compile test using a different simple scenario.
 */
public class CompilePublicTest {

    @Test
    public void simpleCompileTest_publicVariant() {
        // Simulate a compile scenario with enums
        assertEquals(ColorPublic.GREEN, ColorPublic.valueOf("GREEN"));
    }

    enum ColorPublic { RED, GREEN, BLUE }
}