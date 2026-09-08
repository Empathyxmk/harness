package com.zqqqqz2000.shshsh.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class ShellTest {
    static class DummyShell {
        boolean opened = false;
        DummyShell() { opened = true; }
        boolean isOpened() { return opened; }
        void close() { opened = false; }
    }

    @Test
    void testShellOpenAndClose() {
        DummyShell shell = new DummyShell();
        assertTrue(shell.isOpened());
        shell.close();
        assertFalse(shell.isOpened());
    }
}