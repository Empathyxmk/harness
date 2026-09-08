package com.redisgraphpy.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicGraphTest {
    @Test
    void testPublicGraphAddNodesEdges() {
        Graph g = new Graph();
        Node n1 = g.addNode("A", java.util.Map.of("x", 1));
        Node n2 = g.addNode("A", java.util.Map.of("x", 2));
        Edge e = g.addEdge(n1, n2, "R", java.util.Map.of("y", 1));
        assertTrue(g.containsNode(n1));
        assertTrue(g.containsEdge(e));
        assertEquals("R", e.getRelation());
    }
}