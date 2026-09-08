package com.redisgraphpy.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicTestEdge {

    @Test
    void testPublicEdgeEquality() {
        Edge e1 = new Edge(7L, "public-relation", 3L, 4L, java.util.Map.of());
        Edge e2 = new Edge(7L, "public-relation", 3L, 4L, java.util.Map.of());
        assertEquals(e1, e2);
    }
}