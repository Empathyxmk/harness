package com.ovhcelery.dyrygent.original.unit;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import com.ovhcelery.dyrygent.VERSION;
import com.ovhcelery.dyrygent.workflows.*;
import com.ovhcelery.dyrygent.workflows.exceptions.*;

class TestImportsAndVersionTest {

    @Test
    void testVersionValue() {
        assertEquals("0.8.0", VERSION.VERSION);
    }

    @Test
    void testWorkflowsAllExports() {
        assertNotNull(Workflow.class);
        assertNotNull(WorkflowNode.class);
        assertNotNull(WorkflowException.class);
    }

    @Test
    void testExceptionIsException() {
        try {
            throw new WorkflowException("msg");
        } catch (WorkflowException e) {
            assertEquals("msg", e.getMessage());
        }
    }
}