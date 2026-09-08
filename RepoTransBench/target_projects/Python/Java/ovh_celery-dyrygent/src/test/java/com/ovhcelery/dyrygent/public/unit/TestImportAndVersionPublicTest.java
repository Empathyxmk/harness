package com.ovhcelery.dyrygent.public.unit;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import com.ovhcelery.dyrygent.VERSION;
import com.ovhcelery.dyrygent.workflows.*;

class TestImportAndVersionPublicTest {
    @Test
    void testVersionValuePublic() {
        assertArrayEquals(new String[]{"0", "8", "0"}, VERSION.VERSION.split("\\."));
    }
    @Test
    void testWorkflowsAllExportsPublic() {
        assertTrue(Workflow.class.getSimpleName() instanceof String);
        assertTrue(WorkflowNode.class.getSimpleName() instanceof String);
        assertTrue(Exception.class.isAssignableFrom(WorkflowException.class));
    }
    @Test
    void testExceptionIsExceptionPublic() {
        try {
            throw new WorkflowException("different message");
        } catch (WorkflowException e) {
            assertTrue(e.getMessage().contains("different"));
        }
    }
}