package com.ovhcelery.dyrygent.public.component;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import org.mockito.*;

import com.ovhcelery.dyrygent.tasks.WorkflowProcessor;

class TestTasksPublicTest {

    @Test
    void testWorkflowProcessorWithDifferentIds() {
        // Setup mock task obj with request id "feed-face" and retries 4
        TaskObj taskObj = mock(TaskObj.class, RETURNS_DEEP_STUBS);
        when(taskObj.request.id).thenReturn("feed-face");
        when(taskObj.request.retries).thenReturn(4);

        Workflow wf = mock(Workflow.class);
        when(wf.tick()).thenReturn(false);
        when(wf.toDict()).thenReturn(new HashMap<>());
        when(wf.getRetryCountdown()).thenReturn(123);
        wf.workflowOptions = new HashMap<>();

        try(MockedStatic<Workflow> fromDict = mockStatic(Workflow.class)) {
            fromDict.when(() -> Workflow.fromDict(any())).thenReturn(wf);

            // tick returns false, so not retried
            WorkflowProcessor.processor(taskObj, Map.of("foo", "bar"));
            verify(taskObj, never()).retry(any(), anyInt());

            // tick returns true, so should be retried
            when(wf.tick()).thenReturn(true);
            when(wf.getRetryCountdown()).thenReturn(10);
            WorkflowProcessor.processor(taskObj, Map.of("foo", "bar"));
            verify(taskObj).retry(
                argThat(m -> ((Map)m).containsKey("workflow_dict")),
                eq(10)
            );
            assertEquals(3, taskObj.request.retries);
        }
    }
}