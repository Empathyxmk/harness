package com.redisgraphpy.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.List;

class PublicTestPath {

    @Test
    void testPathConstruction() {
        Node n1 = new Node(10L, "Test", java.util.Map.of());
        Node n2 = new Node(11L, "Test", java.util.Map.of());
        Edge e = new Edge(1L, "FOLLOWS", 10L, 11L, java.util.Map.of());
        Path path = new Path(List.of(n1, n2), List.of(e));
        assertEquals(2, path.getNodes().size());
        assertEquals(1, path.getEdges().size());
    }
}