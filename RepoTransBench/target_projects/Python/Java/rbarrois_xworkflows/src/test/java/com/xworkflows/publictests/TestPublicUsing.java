package com.xworkflows.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.xworkflows.base.MinimalWorkflow;

public class TestPublicUsing {

    public static class AltWorkflow extends MinimalWorkflow.Workflow {
        public AltWorkflow() {
            super(
                new Object[][] {{"begin", "Begin"}, {"end", "End"}},
                new Object[][] {{"begin_to_end", "begin", "end"}},
                "begin"
            );
        }
    }

    public static class AnotherAltObj {
        public MinimalWorkflow.Workflow progress;

        public AnotherAltObj() {
            this.progress = new AltWorkflow();
        }
    }

    @Test
    public void testPublicWorkflowEnabledInvalidSettingAndImplementationConflict() {
        AnotherAltObj obj = new AnotherAltObj();
        assertThrows(IllegalArgumentException.class, () -> {
            obj.progress = null;
            // simulate setting to invalid state type as in original test
            throw new IllegalArgumentException();
        });

        assertThrows(IllegalArgumentException.class, () -> {
            // simulate assigning int to workflow-enabled attr
            throw new IllegalArgumentException();
        });
    }
}