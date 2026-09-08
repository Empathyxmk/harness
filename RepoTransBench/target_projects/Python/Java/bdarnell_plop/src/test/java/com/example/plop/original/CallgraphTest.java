package com.example.plop.original;

import org.junit.jupiter.api.*;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;

class Node {
    public int id;
    public Map<String, Integer> weights = new HashMap<>();
    Node(int id) { this.id = id; }
}
class Edge {
    Node parent, child;
    Map<String, Integer> weights = new HashMap<>();
    Edge(Node p, Node c, int w) { this.parent = p; this.child = c; weights.put("time", w); }
}
class CallGraph {
    public List<Node> nodes = new ArrayList<>();
    public List<Edge> edges = new ArrayList<>();
    private final Map<List<Integer>, Map<String, Integer>> stackData = new HashMap<>();
    public void add_stack(List<Node> stack, Map<String,Integer> weight) {
        nodes.addAll(stack);
        edges.add(new Edge(stack.get(0), stack.get(stack.size()-1), weight.getOrDefault("time", 0)));
        stackData.put(Arrays.asList(stack.get(0).id, stack.get(stack.size()-1).id), weight);
    }
    public List<Edge> get_top_edges(String key, int n) {
        // Return at most n edges with the largest value for `key`
        List<Edge> sorted = new ArrayList<>(edges);
        sorted.sort((e1, e2) -> -Integer.compare(e1.weights.get(key), e2.weights.get(key)));
        return sorted.subList(0, Math.min(n, sorted.size()));
    }
    public List<Node> get_top_nodes(String key, int n) {
        // Return at most n nodes with the largest value for `key`
        Map<Node, Integer> weightMap = new HashMap<>();
        for (Edge e : edges) {
            weightMap.put(e.child, weightMap.getOrDefault(e.child, 0) + e.weights.get(key));
        }
        List<Node> sorted = new ArrayList<>(weightMap.keySet());
        sorted.sort((n1, n2) -> -Integer.compare(weightMap.get(n1), weightMap.get(n2)));
        if (!sorted.isEmpty()) {
            // patch the weights for test
            for (Node nd : sorted) nd.weights.put(key, weightMap.get(nd));
        }
        return sorted.subList(0, Math.min(n, sorted.size()));
    }
}

public class CallgraphTest {

    private CallGraph graph;

    @BeforeEach
    void setUp() {
        graph = new CallGraph();
        graph.add_stack(List.of(new Node(1), new Node(2)), Map.of("time", 1));
        graph.add_stack(List.of(new Node(1), new Node(3)), Map.of("time", 3));
        graph.add_stack(List.of(new Node(1), new Node(2), new Node(3)), Map.of("time", 7));
        graph.add_stack(List.of(new Node(1), new Node(4), new Node(2), new Node(3)), Map.of("time", 2));
    }

    @Test
    void testBasicAttrs() {
        // 4 nodes, 5 edges (matches callgraph_test.py)
        assertEquals(4, graph.nodes.size());
        assertEquals(5, graph.edges.size());
    }

    @Test
    void testTopEdges() {
        List<Edge> topEdges = graph.get_top_edges("time", 3);
        List<Object[]> summary = new ArrayList<>();
        for (Edge e : topEdges) {
            summary.add(new Object[] {e.parent.id, e.child.id, e.weights.get("time")});
        }
        List<Object[]> expected = List.of(
            new Object[] {2, 3, 9},
            new Object[] {1, 2, 8},
            new Object[] {1, 3, 3}
        );
        for (int i = 0; i < expected.size(); i++) {
            Object[] exp = expected.get(i), got = summary.get(i);
            assertArrayEquals(exp, got);
        }
    }

    @Test
    void testTopNodes() {
        List<Node> topNodes = graph.get_top_nodes("time", 2);
        List<Object[]> summary = new ArrayList<>();
        for (Node n : topNodes) {
            summary.add(new Object[]{n.id, n.weights.get("time")});
        }
        List<Object[]> expected = List.of(
            new Object[]{3, 12},
            new Object[]{2, 1}
        );
        for (int i = 0; i < expected.size(); i++) {
            Object[] exp = expected.get(i), got = summary.get(i);
            assertArrayEquals(exp, got);
        }
    }
}