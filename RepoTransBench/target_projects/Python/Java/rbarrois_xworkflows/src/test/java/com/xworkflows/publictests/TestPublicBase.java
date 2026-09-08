package com.xworkflows.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

import com.xworkflows.base.MinimalWorkflow;

public class TestPublicBase {

    @Test
    public void testPublicWorkflowStatesAndTransitions() {
        Object[][] states = {
            {"start", "Start"},
            {"mid", "Middle"},
            {"end", "End"}
        };
        Object[][] transitions = {
            {"go_mid", "start", "mid"},
            {"finish", "mid", "end"},
            {"reset", "end", "start"}
        };
        MinimalWorkflow.Workflow wf = new MinimalWorkflow.Workflow(states, transitions, "start");
        assertEquals(3, wf.states.size());
        assertEquals("Start", wf.states.get("start").title);
        assertEquals("start", wf.transitions.get("go_mid").source.get(0).name);
        assertEquals("end", wf.transitions.get("finish").target.name);
        assertEquals(wf.states.get("start"), wf.initialState);
    }

    @Test
    public void testPublicWorkflowInvalidStateTransition() {
        Object[][] states = {
            {"a", "Alpha"},
            {"b", "Beta"}
        };
        Object[][] transitions = {
            {"a_to_b", "a", "b"}
        };
        MinimalWorkflow.Workflow wf = new MinimalWorkflow.Workflow(states, transitions, "a");
        // define inner class for failure
        assertThrows(NullPointerException.class, () -> {
            Object[][] badStates = {
                {"x", "Ex"},
                {"y", "Why"}
            };
            Object[][] badTransitions = {
                {"invalid", "x", "z"}
            };
            new MinimalWorkflow.Workflow(badStates, badTransitions, "x");
        });
    }
}