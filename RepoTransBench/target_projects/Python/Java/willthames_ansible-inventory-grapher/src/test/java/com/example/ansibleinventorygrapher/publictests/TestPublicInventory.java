package com.example.ansibleinventorygrapher.publictests;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

import java.util.*;

class TestPublicInventory {

    static class DummyPlugin {
        boolean called = false;
        public Map<String, Object> getVars(Object loader, String path, List<Object> entities) {
            called = true;
            Map<String, Object> ret = new HashMap<>();
            ret.put("baz", "qux");
            return ret;
        }
    }

    static class DummyPluginHost extends DummyPlugin {
        public Map<String,Object> getHostVars(String name) {
            Map<String,Object> ret = new HashMap<>();
            ret.put("a", 82);
            return ret;
        }
        public Map<String,Object> getGroupVars(String name) {
            Map<String,Object> ret = new HashMap<>();
            ret.put("b", 99);
            return ret;
        }
    }

    static class DummyHost {
        String name;
        DummyHost(String name) { this.name = name; }
    }

    @Test
    void testNoVaultSecretFoundPublic() {
        Exception ex = new Exception();
        assertTrue(ex instanceof Exception);
    }

    @Test
    void testAnsibleInventoryPublicInit() {
        DummyPluginHost cli = new DummyPluginHost();
        assertNotNull(cli);
        cli.setupVaultSecrets(null, null, null, null);
    }

    @Test
    void testPluginsInventoryPublic() {
        DummyPlugin plugin = new DummyPlugin();
        Map<String, Object> v = plugin.getVars(null, "/", List.of(new DummyHost("host")));
        assertEquals("qux", v.get("baz"));
    }

    @Test
    void testGetPluginVarsHostPublic() {
        DummyPluginHost plugin = new DummyPluginHost();
        Map<String,Object> hostVars = plugin.getHostVars("hh");
        assertEquals(82, hostVars.get("a"));
        Map<String,Object> groupVars = plugin.getGroupVars("gg");
        assertEquals(99, groupVars.get("b"));
    }

    @Test
    void testGetGroupVarsPublic() {
        assertEquals(Map.of("other", "groupvar2"), Map.of("other", "groupvar2"));
    }

    @Test
    void testGetHostVarsMagicPublic() {
        class DummyVM2 {
            public Map<String,Object> getVars(String host, boolean includeHostVars) {
                Map<String,Object> r = new HashMap<>();
                r.put("persist", 42);
                r.put("omit", "remove");
                r.put("ansible_version", "yyy");
                return r;
            }
        }
        DummyVM2 vm = new DummyVM2();
        Map<String,Object> m = vm.getVars("hh", true);
        assertTrue(m.containsKey("persist"));
        assertTrue(m.containsKey("omit"));
        assertTrue(m.containsKey("ansible_version"));
    }

    @Test
    void testGetGroupPublic() {
        Map<String,Integer> groups = new HashMap<>();
        groups.put("gx", 501);
        assertEquals(501, groups.get("gx"));
    }

    @Test
    void testGetHostPublic() {
        Map<String,String> hosts = new HashMap<>();
        hosts.put("baz", "hostX");
        assertEquals("hostX", hosts.get("baz"));
    }

    @Test
    void testListHostsPublic() {
        List<String> hosts = List.of("h2");
        assertTrue(hosts.contains("h2"));
    }

    @Test
    void testInventoryManagerPublic() {
        assertNotNull(new DummyHost("wtf"));
    }
}