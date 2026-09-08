package com.redisgraphpy.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class PathTest {
    
    @Test
    void testPathBasic() {
        Node n1 = new Node(1L, "Person", Map.of("name", "Alice"));
        Node n2 = new Node(2L, "Person", Map.of("name", "Bob"));
        Edge e = new Edge(100L, "KNOWS", 1L, 2L, Map.of("since", 2020));
        Path path = new Path(List.of(n1, n2), List.of(e));
        assertEquals(n1, path.getNodes().get(0));
        assertEquals(e, path.getEdges().get(0));
        assertEquals(2, path.length());
    }

    @Test
    void testPathEquals() {
        Node n1 = new Node(1L, "Person", null);
        Node n2 = new Node(2L, "Person", null);
        Edge e = new Edge(10L, "REL", 1L, 2L, null);
        Path p1 = new Path(List.of(n1, n2), List.of(e));
        Path p2 = new Path(List.of(n1, n2), List.of(e));
        assertEquals(p1, p2);
    }
}