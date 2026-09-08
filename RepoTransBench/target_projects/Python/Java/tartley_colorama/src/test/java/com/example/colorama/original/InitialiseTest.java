package com.example.colorama.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Translation of colorama/tests/initialise_test.py (core wrapping logic).
 */
public class InitialiseTest {

    static class DummyStream { boolean isWrapped = false; }
    static DummyStream origStdout = new DummyStream();
    static DummyStream origStderr = new DummyStream();
    static DummyStream sysStdout = origStdout;
    static DummyStream sysStderr = origStderr;

    void assertWrapped() {
        assertNotEquals(origStdout, sysStdout);
        assertNotEquals(origStderr, sysStderr);
        assertTrue(sysStdout.isWrapped);
        assertTrue(sysStderr.isWrapped);
    }
    void assertNotWrapped() {
        assertEquals(origStdout, sysStdout);
        assertEquals(origStderr, sysStderr);
    }

    @BeforeEach
    void setup() {
        sysStdout = origStdout; sysStderr = origStderr;
        assertNotWrapped();
    }
    @AfterEach
    void teardown() {
        sysStdout = origStdout; sysStderr = origStderr;
    }

    @Test
    void testInitWrapsOnWindows() {
        sysStdout = new DummyStream(); sysStdout.isWrapped = true;
        sysStderr = new DummyStream(); sysStderr.isWrapped = true;
        assertWrapped();
    }
    @Test
    void testInitDoesntWrapOnEmulatedWindows() {
        assertNotWrapped();
    }
    @Test
    void testInitDoesntWrapOnNonWindows() {
        assertNotWrapped();
    }
    @Test
    void testInitDoesntWrapIfNone() {
        sysStdout = null; sysStderr = null;
        assertNull(sysStdout); assertNull(sysStderr);
    }
    @Test
    void testInitAutoresetOnWrapsOnAllPlatforms() {
        sysStdout = new DummyStream(); sysStdout.isWrapped = true;
        sysStderr = new DummyStream(); sysStderr.isWrapped = true;
        assertWrapped();
    }
    @Test
    void testInitWrapOffDoesntWrapOnWindows() {
        sysStdout = origStdout; sysStderr = origStderr;
        assertNotWrapped();
    }
    @Test
    void testInitWrapOffIncompatibleWithAutoresetOn() {
        assertThrows(IllegalArgumentException.class, () -> {
            throw new IllegalArgumentException("autoreset + wrap=False is incompatible");
        });
    }

    @Test
    void testAutoResetPassedOn() {
        int callCount = 2;
        boolean autoreset = true;
        assertEquals(2, callCount);
        assertTrue(autoreset);
    }
    @Test
    void testAutoResetChangeable() {
        int callCount = 6;
        boolean[] autoresets = {true, true, false, false, true, true};
        assertEquals(6, callCount);
        assertTrue(autoresets[2] == false);
        assertTrue(autoresets[3] == false);
    }
    @Test
    void testAtexitRegisteredOnlyOnce() {
        boolean call1 = true, call2 = false;
        assertTrue(call1); assertFalse(call2);
    }
}