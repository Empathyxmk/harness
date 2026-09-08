package com.spotify.pythonflow.original;

import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

public class CoreBasicTest {

    public static class Graph {
        public Map<String, Operation> operations = new HashMap<>();
        public Graph() { }
        public void add(Operation op) {
            operations.put(op.name, op);
        }
    }

    public static abstract class Operation {
        public final String name;
        public final Graph graph;
        public Operation(String name, Graph g) {
            this.name = name;
            this.graph = g;
        }
        protected abstract Object evaluate();
    }

    public static class ConstOp extends Operation {
        private final Object value;
        public ConstOp(String name, Graph g, Object v) {
            super(name, g);
            this.value = v;
        }
        @Override
        protected Object evaluate() { return value; }
    }

    public static class AddOp extends Operation {
        private final Operation a, b;
        public AddOp(String name, Graph g, Operation a, Operation b) {
            super(name, g);
            this.a = a; this.b = b;
        }
        @Override
        protected Object evaluate() {
            return ((Number)a.evaluate()).intValue() + ((Number)b.evaluate()).intValue();
        }
    }

    @Test
    public void testGraphAddAndOperationEvaluate() {
        Graph g = new Graph();
        Operation constA = new ConstOp("a", g, 3);
        Operation constB = new ConstOp("b", g, 5);
        g.add(constA);
        g.add(constB);
        Operation add = new AddOp("add", g, constA, constB);
        g.add(add);
        assertEquals(8, add.evaluate());
    }

    @Test
    public void testOperationNamingAndRegistry() {
        Graph g = new Graph();
        Operation c = new ConstOp("const1", g, 10);
        g.add(c);
        assertSame(c, g.operations.get("const1"));
        assertEquals("const1", c.name);
    }

    @Test
    public void testOperationReturnsExpectedValue() {
        Graph g = new Graph();
        Operation c = new ConstOp("x", g, 12);
        assertEquals(12, c.evaluate());
        Operation c2 = new ConstOp("y", g, 7);
        Operation add = new AddOp("z", g, c, c2);
        assertEquals(19, add.evaluate());
    }
}