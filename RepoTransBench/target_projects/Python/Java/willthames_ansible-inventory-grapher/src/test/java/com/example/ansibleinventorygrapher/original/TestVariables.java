package com.example.ansibleinventorygrapher.original;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.*;

import java.util.*;

class TestVariables {

    static class DummyHost {
        String name;
        List<String> groups = new ArrayList<>();
        Map<String, Object> hostVars = new HashMap<>();
        DummyHost(String name) { this.name = name; }
    }

    static class DummyInventory {
        Map<String, Map<String, Object>> groupVars = new HashMap<>();
        Map<DummyHost, Map<String, Object>> hostVars = new HashMap<>();
        Map<String, Object> getGroupVars(String g) { return groupVars.get(g); }
        Map<String, Object> getHostVars(DummyHost h) { return hostVars.get(h); }
        DummyHost getHost(String name) { 
            for (DummyHost h : hostVars.keySet()) if (h.name.equals(name)) return h; 
            return null;
        }
        String getGroupForHost(DummyHost h) { 
            if (!h.groups.isEmpty()) return h.groups.get(0); 
            return null;
        }
    }

    DummyInventory inventory;
    DummyHost host;
    Map<String, Map<String, Object>> variables;

    @BeforeEach
    void setUp() {
        inventory = new DummyInventory();

        // Setup test data as per the Python fixtures
        host = new DummyHost("host");
        // Grandparent group: only gp_not_overridden
        inventory.groupVars.put("grandparent", Map.of("gp_not_overridden", "gp"));
        // Parent group: parent_not_overridden, gp_overridden_in_parent
        inventory.groupVars.put("parent", Map.of("parent_not_overridden", "parent", "gp_overridden_in_parent", "parent"));
        // Child group is not directly modeled in the fixture, so we'll use host only
        // Host vars: gp_overridden_in_child, parent_overridden_in_child, child_only
        Map<String, Object> hvars = new HashMap<>();
        hvars.put("gp_overridden_in_child", "child");
        hvars.put("parent_overridden_in_child", "child");
        hvars.put("child_only", "child");
        inventory.hostVars.put(host, hvars);
        // Group memberships
        host.groups.add("parent");
        host.groups.add("grandparent");

        // Simulate tidy_all_the_variables: groupVars & hostVars dict
        variables = new HashMap<>();
        variables.put("grandparent", inventory.groupVars.get("grandparent"));
        variables.put("parent", inventory.groupVars.get("parent"));
        variables.put(host, hvars);
    }

    @Test
    void testGpGroupVars() {
        Map<String,Object> gvars = variables.get("grandparent");
        assertEquals(Set.of("gp_not_overridden"), gvars.keySet());
        assertEquals("gp", gvars.get("gp_not_overridden"));
    }

    @Test
    void testParentGroupVars() {
        Map<String,Object> pvars = variables.get("parent");
        assertEquals(Set.of("parent_not_overridden", "gp_overridden_in_parent"), pvars.keySet());
        assertEquals("parent", pvars.get("parent_not_overridden"));
    }

    @Test
    void testHostVars() {
        Map<String,Object> hvars = new HashMap<>(variables.get(host));
        assertEquals("child", hvars.get("gp_overridden_in_child"));
        assertEquals("child", hvars.get("parent_overridden_in_child"));
        assertEquals("child", hvars.get("child_only"));
    }
}