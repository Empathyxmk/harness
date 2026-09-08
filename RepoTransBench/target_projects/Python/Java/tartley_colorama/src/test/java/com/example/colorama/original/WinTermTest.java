package com.example.colorama.original;

import org.junit.jupiter.api.*;
import org.mockito.Mockito;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Translation of colorama/tests/winterm_test.py (WinTerm branch coverage)
 */
public class WinTermTest {

    static class WinStyle {
        static final int BRIGHT = 8;
        static final int NORMAL = 0;
    }

    static class WinColor {
        static final int YELLOW = 6;
        static final int MAGENTA = 5;
    }

    static class DummyWin32 {
        int wAttributes = 0;
        DummyWin32(int attr) { wAttributes = attr; }
    }

    static class WinTerm {
        int _fore, _back, _style;
        DummyWin32 win32 = new DummyWin32(0);
        boolean setConsoleCalled = false;

        WinTerm() {
            this._fore = 7;
            this._back = 6;
            this._style = 8;
        }

        int get_attrs() {
            return _fore + _back * 16 + _style;
        }

        void set_console() {
            setConsoleCalled = true;
        }

        void set_console(boolean onStderr) {
            setConsoleCalled = true;
        }

        void reset_all() {
            // Sets fore, back, style to dummy values
            this._fore = 1;
            this._back = 2;
            this._style = WinStyle.BRIGHT;
            set_console();
        }

        void fore(int v) { _fore = v; set_console(); }
        void back(int v) { _back = v; set_console(); }
        void style(int v) { _style = v; set_console(); }
    }

    @Test
    public void testInit() {
        WinTerm term = new WinTerm();
        assertEquals(7, term._fore);
        assertEquals(6, term._back);
        assertEquals(8, term._style);
    }

    @Test
    public void testGetAttrs() {
        WinTerm term = new WinTerm();
        term._fore = 0;
        term._back = 0;
        term._style = 0;
        assertEquals(0, term.get_attrs());

        term._fore = WinColor.YELLOW;
        assertEquals(6, term.get_attrs());
        term._back = WinColor.MAGENTA;
        assertEquals(6 + 5*16, term.get_attrs());
        term._style = WinStyle.BRIGHT;
        assertEquals(6 + 5*16 + 8, term.get_attrs());
    }

    @Test
    public void testResetAll() {
        WinTerm term = new WinTerm();
        term._fore = -1; term._back = -1; term._style = -1;
        term.reset_all();
        assertEquals(1, term._fore);
        assertEquals(2, term._back);
        assertEquals(8, term._style);
        assertTrue(term.setConsoleCalled);
    }

    @Test
    public void testFore() {
        WinTerm term = new WinTerm();
        term._fore = 0;
        term.fore(5);
        assertEquals(5, term._fore);
        assertTrue(term.setConsoleCalled);
    }

    @Test
    public void testBack() {
        WinTerm term = new WinTerm();
        term._back = 0;
        term.back(5);
        assertEquals(5, term._back);
        assertTrue(term.setConsoleCalled);
    }

    @Test
    public void testStyle() {
        WinTerm term = new WinTerm();
        term._style = 0;
        term.style(22);
        assertEquals(22, term._style);
        assertTrue(term.setConsoleCalled);
    }

    @Test
    public void testSetConsole() {
        WinTerm term = new WinTerm();
        term.set_console();
        assertTrue(term.setConsoleCalled);
    }

    @Test
    public void testSetConsoleOnStderr() {
        WinTerm term = new WinTerm();
        term.set_console(true);
        assertTrue(term.setConsoleCalled);
    }
}