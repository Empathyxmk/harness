package com.nickstenning.honcho.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.nickstenning.honcho.Manager;

class TestManager {

    @Test
    void testManagerAddProcess() {
        Manager manager = new Manager();
        manager.addProcess("web", "python app.py");
        assertTrue(manager.hasProcess("web"));
    }
}