package com.redisgraphpy.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class EdgeTest {

    @Test
    void testEdgeEquality() {
        Edge edge1 = new Edge(1L, "rel", 2L, 3L, null);
        Edge edge2 = new Edge(1L, "rel", 2L, 3L, null);
        assertEquals(edge1, edge2);
    }

    @Test
    void testEdgeInequality() {
        Edge edge = new Edge(1L, "rel", 2L, 3L, null);
        Node otherNode = new Node(1L, "node", null);
        assertNotEquals(edge, otherNode);
    }

    @Test
    void testEdgeToStringAndHashCode() {
        Edge edge = new Edge(1L, "rel", 2L, 3L, null);
        String repr = edge.toString();
        assertNotNull(repr);
        int hash1 = edge.hashCode();
        int hash2 = edge.hashCode();
        assertEquals(hash1, hash2);
    }
}