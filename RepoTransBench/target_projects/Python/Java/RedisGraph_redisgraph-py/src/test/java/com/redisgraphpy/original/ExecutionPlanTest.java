package com.redisgraphpy.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class ExecutionPlanTest {

    @Test
    void testExecutionPlanGetRoot() {
        ExecutionPlan plan = ExecutionPlan.parse("Project\n\tScan");
        assertEquals("Project", plan.getRootOperation().getName());
    }

    @Test
    void testExecutionPlanFormat() {
        String planString = "Project\n\tScan";
        ExecutionPlan plan = ExecutionPlan.parse(planString);
        assertEquals(planString, plan.format());
    }

    @Test
    void testExecutionPlanEquals() {
        ExecutionPlan plan1 = ExecutionPlan.parse("Project\n\tScan");
        ExecutionPlan plan2 = ExecutionPlan.parse("Project\n\tScan");
        assertEquals(plan1, plan2);
    }

    @Test
    void testExecutionPlanInequality() {
        ExecutionPlan plan1 = ExecutionPlan.parse("Project\n\tScan");
        ExecutionPlan plan2 = ExecutionPlan.parse("Filter\n\tScan");
        assertNotEquals(plan1, plan2);
    }
}