// Extra test file for test_edge.py if not covered yet.
package com.redisgraphpy.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestEdge {

    @Test
    void testEdgeRelInitialization() {
        Edge edge = new Edge(100L, "REL_TYPE", 1L, 2L, java.util.Map.of());
        assertEquals(100L, edge.getId());
        assertEquals("REL_TYPE", edge.getRelation());
        assertEquals(1L, edge.getSourceId());
        assertEquals(2L, edge.getDestinationId());
    }
}