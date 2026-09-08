package com.nickstenning.honcho.public_;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.nickstenning.honcho.Manager;

class TestPublicManager {

    @Test
    void testPublicManagerAddProcess() {
        Manager manager = new Manager();
        manager.addProcess("web", "python app.py");
        assertTrue(manager.hasProcess("web"));
    }
}