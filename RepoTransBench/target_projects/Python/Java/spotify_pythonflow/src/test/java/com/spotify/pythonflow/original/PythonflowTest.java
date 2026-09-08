package com.spotify.pythonflow.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

import java.util.concurrent.atomic.AtomicInteger;

public class PythonflowTest {

    static class AddOperation extends CoreBasicTest.Operation {
        private final int a, b;
        public AddOperation(String name, CoreBasicTest.Graph g, int a, int b) {
            super(name, g);
            this.a = a; this.b = b;
        }
        @Override
        protected Object evaluate() {
            return a + b;
        }
    }

    @Test
    public void testSimpleAddOp() {
        CoreBasicTest.Graph g = new CoreBasicTest.Graph();
        AddOperation op = new AddOperation("add1", g, 2, 3);
        assertEquals(5, op.evaluate());
    }

    @Test
    public void testOperationEvaluationConsistency() {
        CoreBasicTest.Graph g = new CoreBasicTest.Graph();
        AddOperation op = new AddOperation("add2", g, 10, 32);
        assertTrue(op.evaluate() instanceof Integer);
        assertEquals(42, op.evaluate());
    }

    @Test
    public void testGraphOperationRegistrationAndNameUniqueness() {
        CoreBasicTest.Graph g = new CoreBasicTest.Graph();
        AddOperation op1 = new AddOperation("op", g, 1, 1);
        g.operations.put("op", op1);
        assertSame(op1, g.operations.get("op"));
        AddOperation op2 = new AddOperation("op", g, 2, 2);
        g.operations.put("op", op2);
        // Should overwrite
        assertSame(op2, g.operations.get("op"));
    }
}