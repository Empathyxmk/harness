package com.redisgraphpy.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class GraphTest {

    @Test
    void testNodeCreation() {
        Node node = new Node(1L, "Person", Map.of("name", "Alice"));
        assertEquals(1L, node.getId());
        assertEquals("Person", node.getLabel());
        assertEquals("Alice", node.getProperty("name"));
    }

    @Test
    void testGraphAddNodeAndEdge() {
        Graph graph = new Graph();
        Node n1 = graph.addNode("Person", Map.of("name", "Alice"));
        Node n2 = graph.addNode("Person", Map.of("name", "Bob"));
        Edge edge = graph.addEdge(n1, n2, "KNOWS", Map.of("since", 2020));
        assertTrue(graph.containsNode(n1));
        assertTrue(graph.containsEdge(edge));
        assertEquals("KNOWS", edge.getRelation());
        assertEquals(n2, edge.getDestinationNode());
    }

    @Test
    void testNodeEquality() {
        Node n1 = new Node(1L, "Person", Map.of("x", 1));
        Node n2 = new Node(1L, "Person", Map.of("x", 1));
        assertEquals(n1, n2);
    }
}