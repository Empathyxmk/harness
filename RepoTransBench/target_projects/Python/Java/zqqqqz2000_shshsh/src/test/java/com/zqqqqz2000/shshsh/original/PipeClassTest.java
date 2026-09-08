package com.zqqqqz2000.shshsh.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class PipeClassTest {
    static class Pipe {
        int value = 44;

        int getValue() {
            return value;
        }

        void setValue(int v) {
            value = v;
        }
    }

    @Test
    void testPipeClassGetSetValue() {
        Pipe pipe = new Pipe();
        assertEquals(44, pipe.getValue());
        pipe.setValue(88);
        assertEquals(88, pipe.getValue());
    }
}