package com.redisgraphpy.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicExecutionPlanTest {
    @Test
    void testPublicExecutionPlan() {
        ExecutionPlan plan = ExecutionPlan.parse("Project\n\tScan");
        assertEquals("Project", plan.getRootOperation().getName());
        assertEquals("Project\n\tScan", plan.format());
    }
}