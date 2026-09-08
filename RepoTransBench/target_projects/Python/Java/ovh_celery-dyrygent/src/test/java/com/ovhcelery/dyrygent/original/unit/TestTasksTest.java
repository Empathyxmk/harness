package com.ovhcelery.dyrygent.original.unit;

import org.junit.jupiter.api.*;
import org.mockito.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

// Assume the Java API structure similarly mimics Python structure
import com.ovhcelery.dyrygent.tasks;
import com.ovhcelery.dyrygent.workflows.Workflow;

class TestTasksTest {

    @Mock
    private Workflow wf;

    @Mock
    private Object taskObj;

    @BeforeEach
    void setup() {
        MockitoAnnotations.openMocks(this);
        // Simulate a Task with a 'request' that has id and retries
        taskObj = mock(Object.class, RETURNS_DEEP_STUBS);
        // Use deep stubs to allow taskObj.request.id/retries
        when(taskObj.toString()).thenReturn("task");
        when(taskObj.getClass().getSimpleName()).thenReturn("task");
        when(taskObj.request.id).thenReturn("dead-beef");
        when(taskObj.request.retries).thenReturn(1);
    }

    @Test
    void testWorkflowProcessor() {
        // Patch Workflow.fromDict to return our workflow mock
        try (MockedStatic<Workflow> fromDictMock = mockStatic(Workflow.class)) {
            fromDictMock.when(() -> Workflow.fromDict(any())).thenReturn(wf);
            // Setup wf methods
            when(wf.tick()).thenReturn(false);
            when(wf.toDict()).thenReturn(new java.util.HashMap<>());
            when(wf.getRetryCountdown()).thenReturn(42);
            wf.workflowOptions = new java.util.HashMap<>();
            // Test: workflow_processor should call tick and not call retry
            tasks.workflowProcessor(taskObj, java.util.Map.of("a", "b"));
            fromDictMock.verify(() -> Workflow.fromDict(
                argThat(m -> ((java.util.Map)m).get("a").equals("b")
                     && ((java.util.Map)m).get("id").equals("dead-beef"))
            ));
            verify(wf).tick();
            verify(taskObj, never()).retry(any(), any());

            // Next, set tick to true, simulate retries
            when(wf.tick()).thenReturn(true);
            when(wf.getRetryCountdown()).thenReturn(7);

            tasks.workflowProcessor(taskObj, java.util.Map.of("a", "b"));
            // Should call retry this time
            verify(taskObj).retry(
                argThat(kwargs -> ((java.util.Map)kwargs).containsKey("workflow_dict")),
                eq(7)
            );
            assertEquals(0, taskObj.request.retries);
        }
    }
}