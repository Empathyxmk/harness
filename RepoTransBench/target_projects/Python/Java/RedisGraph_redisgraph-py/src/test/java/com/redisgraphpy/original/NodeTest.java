package com.redisgraphpy.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class NodeTest {

    @Test
    void testNodeProperties() {
        Node node = new Node(1L, "Person", Map.of("name", "Eve", "age", 30));
        assertEquals("Eve", node.getProperty("name"));
        assertEquals(30, node.getProperty("age"));
    }

    @Test
    void testNodeToStringAndHashCode() {
        Node node = new Node(2L, "User", null);
        assertNotNull(node.toString());
        int h1 = node.hashCode();
        int h2 = node.hashCode();
        assertEquals(h1, h2);
    }
}