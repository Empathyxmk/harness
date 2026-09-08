package com.nickstenning.honcho.public_;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.nickstenning.honcho.Process;

class TestPublicProcess {

    @Test
    void testPublicProcessHasName() {
        Process proc = new Process("worker", "python worker.py");
        assertEquals("worker", proc.getName());
    }
}