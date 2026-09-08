package com.nickstenning.honcho.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.nickstenning.honcho.Process;

class TestProcess {

    @Test
    void testProcessHasName() {
        Process proc = new Process("worker", "python worker.py");
        assertEquals("worker", proc.getName());
    }
}