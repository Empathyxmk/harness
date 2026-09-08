// Extra test for test_node.py if needed for missing coverage
package com.redisgraphpy.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestNode {

    @Test
    void testNodeLabelIdentity() {
        Node n = new Node(5L, "Category", java.util.Map.of("score", 100));
        assertEquals("Category", n.getLabel());
        assertEquals(100, n.getProperty("score"));
    }
}