package com.example.colorama.public_tests;

import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Java translation of public_tests/test_public_winterm.py
 * Simulating WinTerm logic and field computations.
 */
public class PublicWinTermTest {

    static class DummyAttr {
        public int wAttributes;
        public DummyAttr(int wAttributes) { this.wAttributes = wAttributes; }
    }

    static class WinTermFake {
        int _fore;
        int _back;
        int _style;

        WinTermFake(int wAttributes) {
            this._fore = wAttributes & 7;
            this._back = (wAttributes >> 4) & 7;
            this._style = wAttributes & ~0x77;
        }

        void reset_all(DummyAttr attr) {
            this._fore = attr.wAttributes & 7;
            this._back = (attr.wAttributes >> 4) & 7;
            this._style = attr.wAttributes & ~0x77;
        }
    }

    @Test
    public void testInit_public() {
        // wAttributes = 171 -> 0b10101011
        DummyAttr attr = new DummyAttr(171);
        WinTermFake term = new WinTermFake(attr.wAttributes);
        assertEquals(3, term._fore);
        assertEquals(2, term._back);
        assertEquals(136, term._style);
    }

    @Test
    public void testResetAll_public() {
        // wAttributes = 250 -> 0b11111010
        DummyAttr attr = new DummyAttr(250);
        WinTermFake term = new WinTermFake(0);
        term._fore = 1;
        term._back = 3;
        term._style = 0;
        term.reset_all(attr);
        assertEquals(2, term._fore);
        assertEquals(7, term._back);
        assertEquals(136, term._style);
    }
}