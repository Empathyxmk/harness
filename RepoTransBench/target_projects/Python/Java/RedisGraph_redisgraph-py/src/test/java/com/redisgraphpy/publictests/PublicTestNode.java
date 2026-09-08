package com.redisgraphpy.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicTestNode {

    @Test
    void testPublicNodeProperties() {
        Node node = new Node(99L, "testLabel", java.util.Map.of("hello", "world"));
        assertEquals("testLabel", node.getLabel());
        assertEquals("world", node.getProperty("hello"));
    }
}