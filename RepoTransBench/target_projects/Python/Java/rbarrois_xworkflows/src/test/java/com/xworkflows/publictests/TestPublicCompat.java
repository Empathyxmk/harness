package com.xworkflows.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestPublicCompat {

    public static class Workflow {
        // Mimics base.Workflow with states attribute
        public static String __name__ = "Workflow";
    }

    @Test
    public void testPublicStringTypeIsStr() {
        assertTrue(Workflow.__name__ instanceof String);
    }

    @Test
    public void testPublicBaseWorkflowHasStates() {
        // A custom workflow with states
        class AltCompWorkflow {
            public static java.util.Map<String, String> states = new java.util.HashMap<>();
            public static {
                states.put("alpha", "Alpha");
                states.put("beta", "Beta");
            }
        }
        assertTrue(AltCompWorkflow.states.containsKey("alpha"));
        assertEquals("Beta", AltCompWorkflow.states.get("beta"));
    }
}