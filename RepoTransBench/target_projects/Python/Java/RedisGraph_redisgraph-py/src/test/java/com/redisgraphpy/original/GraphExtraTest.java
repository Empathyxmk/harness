package com.redisgraphpy.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class GraphExtraTest {

    @Test
    void testGraphNodesIteration() {
        Graph graph = new Graph();
        Node n1 = graph.addNode("Person", Map.of("name", "Alice"));
        Node n2 = graph.addNode("Person", Map.of("name", "Bob"));
        List<Node> nodes = new ArrayList<>();
        for (Node n : graph.getNodes()) {
            nodes.add(n);
        }
        assertTrue(nodes.contains(n1) && nodes.contains(n2));
    }

    @Test
    void testGraphEdgesIteration() {
        Graph graph = new Graph();
        Node n1 = graph.addNode("Person", Map.of("name", "Alice"));
        Node n2 = graph.addNode("Person", Map.of("name", "Bob"));
        Edge edge = graph.addEdge(n1, n2, "KNOWS", Map.of("since", 2020));
        List<Edge> edges = new ArrayList<>();
        for (Edge e : graph.getEdges()) {
            edges.add(e);
        }
        assertTrue(edges.contains(edge));
    }
}