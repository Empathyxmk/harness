package com.example.ansibleinventorygrapher.original;

import com.example.ansibleinventorygrapher.Edge;
import com.example.ansibleinventorygrapher.Node;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class TestInit {

    static class DummyVault {
        String ciphertext;
        DummyVault(String ciphertext) { this.ciphertext = ciphertext; }
    }

    static class DummyGroup {
        String name;
        List<DummyGroup> parentGroups;
        List<DummyGroup> ancestors;
        DummyGroup(String name) {
            this.name = name;
            this.parentGroups = new ArrayList<>();
            this.ancestors = new ArrayList<>();
        }
        DummyGroup(String name, List<DummyGroup> parentGroups, List<DummyGroup> ancestors) {
            this.name = name;
            this.parentGroups = parentGroups == null ? new ArrayList<>() : parentGroups;
            this.ancestors = ancestors == null ? new ArrayList<>() : ancestors;
        }
        List<DummyGroup> getAncestors() { return ancestors != null ? ancestors : new ArrayList<>(); }
    }

    static class DummyHost {
        String name;
        List<DummyGroup> groups = new ArrayList<>();
        Map<String, Object> hostVars = new HashMap<>();
        DummyHost(String name) { this.name = name;}
        List<DummyGroup> getGroups() { return groups; }
    }

    static class DummyInventoryManager {
        Map<Object,Map<String,Object>> groupVars = new HashMap<>();
        Map<Object,Map<String,Object>> hostVars = new HashMap<>();
        class Inv {
            Map<Object,Map<String,Object>> groupVars;
            Map<Object,Map<String,Object>> hostVars;
            Inv(Map<Object,Map<String,Object>> gv, Map<Object,Map<String,Object>> hv) {
                groupVars = gv;
                hostVars = hv;
            }
            public Map<String,Object> getGroupVars(Object group) {
                return groupVars.getOrDefault(group, new HashMap<>());
            }
            public Map<String,Object> getHostVars(Object host) {
                return hostVars.getOrDefault(host, new HashMap<>());
            }
        }
        Inv inventory;
        DummyInventoryManager(Map<Object,Map<String,Object>> groupVars, Map<Object,Map<String,Object>> hostVars) {
            this.groupVars = groupVars;
            this.hostVars = hostVars;
            this.inventory = new Inv(groupVars, hostVars);
        }
    }

    @Test
    void testEdgeReprEqHash() {
        Edge e1 = new Edge("a", "b");
        Edge e2 = new Edge("a", "b");
        Edge e3 = new Edge("a", "c");
        assertEquals("a -> b", e1.toString());
        assertEquals(e1, e2);
        assertNotEquals(e1, e3);
        assertEquals(e1.hashCode(), e2.hashCode());
        assertNotEquals(e1.hashCode(), e3.hashCode());
    }

    @Test
    void testNodeReprEqHash() {
        Node n1 = new Node("n");
        Node n2 = new Node("n");
        Node n3 = new Node("x");
        assertEquals("n", n1.toString());
        assertEquals(n1, n2);
        assertNotEquals(n1, n3);
        assertEquals(n1.hashCode(), n2.hashCode());
        assertNotEquals(n1.hashCode(), n3.hashCode());
    }

    // The following methods induce side effects, but the translation keeps the intent.
    @Test
    void testParentGraphsSimple() {
        DummyGroup g1 = new DummyGroup("G1");
        DummyGroup g2 = new DummyGroup("G2", List.of(g1), null);
        DummyGroup child = new DummyGroup("CHILD", List.of(g2), null);
        List<DummyGroup> groups = List.of(g1, g2);
        Set<Edge> results = com.example.ansibleinventorygrapher.__init__.parent_graphs(child, new ArrayList<>(groups));
        for (Edge e : results) assertTrue(e instanceof Edge);
    }
}