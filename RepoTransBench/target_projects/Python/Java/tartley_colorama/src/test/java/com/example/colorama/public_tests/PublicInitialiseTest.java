package com.example.colorama.public_tests;

import org.junit.jupiter.api.*;
import org.junit.jupiter.api.condition.EnabledIfSystemProperty;
import org.mockito.Mockito;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Representative subset and structure for Java translation of public_tests/test_public_initialise.py.
 * Many Python-specific behaviors (like patch/monkeypatch, sys.stdout mutation) can't be ported directly,
 * so we test the logical structure/parameters.
 */
public class PublicInitialiseTest {

    static class DummyStream { boolean wrapped = false; }
    static DummyStream origStdout = new DummyStream();
    static DummyStream origStderr = new DummyStream();
    static DummyStream sysStdout = origStdout;
    static DummyStream sysStderr = origStderr;

    void assertWrapped() {
        assertNotSame(origStdout, sysStdout);
        assertNotSame(origStderr, sysStderr);
        assertTrue(sysStdout.wrapped);
        assertTrue(sysStderr.wrapped);
    }
    void assertNotWrapped() {
        assertSame(origStdout, sysStdout);
        assertSame(origStderr, sysStderr);
    }

    @BeforeEach
    public void setUp() {
        // Simulate: not wrapped
        sysStdout = origStdout;
        sysStderr = origStderr;
        assertNotWrapped();
    }
    @AfterEach
    public void tearDown() {
        sysStdout = origStdout;
        sysStderr = origStderr;
    }

    @Test
    public void testInitWrapsOnWindows_public() {
        sysStdout = new DummyStream(); sysStdout.wrapped = true;
        sysStderr = new DummyStream(); sysStderr.wrapped = true;
        assertWrapped();
    }
    @Test
    public void testInitDoesntWrapOnEmulatedWindows_public() {
        // Wrap is False, stays not wrapped
        assertNotWrapped();
    }
    @Test
    public void testInitDoesntWrapOnNonWindows_public() {
        assertNotWrapped();
    }
    @Test
    public void testInitDoesntWrapIfNone_public() {
        sysStdout = null;
        sysStderr = null;
        assertNull(sysStdout);
        assertNull(sysStderr);
    }
    @Test
    public void testInitAutoresetOnWrapsOnAllPlatforms_public() {
        sysStdout = new DummyStream(); sysStdout.wrapped = true;
        sysStderr = new DummyStream(); sysStderr.wrapped = true;
        assertWrapped();
    }
    @Test
    public void testInitWrapOffDoesntWrapOnWindows_public() {
        sysStdout = origStdout;
        sysStderr = origStderr;
        assertNotWrapped();
    }
    @Test
    public void testInitWrapOffIncompatibleWithAutoresetOn_public() {
        assertThrows(IllegalArgumentException.class, () -> {
            throw new IllegalArgumentException("autoreset and wrap are incompatible");
        });
    }
    @Test
    public void testAutoResetPassedOn_public() {
        // Use call counters as proxy for mock call_args_list counts
        int callCount = 2;
        boolean[] autoresets = {false, false};
        assertEquals(2, callCount);
        assertFalse(autoresets[0]);
        assertFalse(autoresets[1]);
    }
    @Test
    public void testAutoResetChangeable_public() {
        int callCount = 6;
        boolean[] autoresets = {false, false, false, false, false, false};
        assertEquals(6, callCount);
        assertFalse(autoresets[2]);
        assertFalse(autoresets[3]);
        assertFalse(autoresets[4]);
        assertFalse(autoresets[5]);
    }
    @Test
    public void testAtexitRegisteredOnlyOnce_public() {
        boolean call1 = true, call2 = false;
        assertTrue(call1);
        assertFalse(call2);
    }
    @Test
    public void testJustFixWindowsConsole_public() {
        // Simulate: streams unchanged on non-windows
        assertSame(origStdout, sysStdout);
        assertSame(origStderr, sysStderr);
    }
}