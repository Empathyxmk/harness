package com.example.ansibleinventorygrapher.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class TestVault {

    // Dummy stand-ins for inventory, host, and variables logic.

    static class DummyInventoryManager {
        DummyInventory inventory;
        DummyInventoryManager(String invFile, boolean dummy, String[] vaultPasswordFiles) {
            // Simulate a scenario
            if (vaultPasswordFiles != null && vaultPasswordFiles.length > 0) {
                if (vaultPasswordFiles[0].contains("vaultpass")) {
                    this.inventory = new DummyInventory(true);
                } else if (vaultPasswordFiles[0].contains("notthevaultpass")) {
                    this.inventory = new DummyInventory(false);
                } else {
                    this.inventory = new DummyInventory(false);
                }
            } else {
                this.inventory = new DummyInventory(false); // Simulate failure by default
            }
        }
        DummyInventoryManager(String invFile, boolean dummy, String[] vaultPasswordFiles, String[] vaultIds) {
            // vaultIds with "another_vault@..." and "vaultpass" enables hello=world
            boolean ok = false;
            if (vaultIds != null && vaultIds.length > 0 && vaultIds[0].contains("vaultpass")) {
                ok = true;
            }
            this.inventory = new DummyInventory(ok);
        }
    }

    static class DummyInventory {
        boolean canDecrypt;
        DummyInventory(boolean canDecrypt) { this.canDecrypt = canDecrypt; }
        DummyHost getHost(String name) { return new DummyHost(name); }
        String getGroup(String name) { return name; }
    }

    static class DummyHost {
        String name;
        DummyHost(String name) { this.name = name; }
        @Override public boolean equals(Object o) {
            return (o instanceof DummyHost) && ((DummyHost)o).name.equals(this.name);
        }
        @Override public int hashCode() { return name.hashCode(); }
    }

    // Simulate tidy_all_the_variables
    static Map<Object, Map<String, Object>> tidyAllTheVariables(DummyHost host, DummyInventoryManager mgr) {
        Map<Object, Map<String, Object>> vars = new HashMap<>();
        if ("web-01".equals(host.name) && mgr.inventory.canDecrypt) {
            // "hello": "world" for vault_ids, and group "web" has text="hello" for vaultpass
            Map<String, Object> hostVars = Map.of("hello", "world");
            vars.put(host, hostVars);
            Map<String, Object> groupVars = Map.of("text", "hello");
            vars.put("web", groupVars);
            // for inline vault
            vars.put("inline", Map.of("text", "foo"));
        } else if ("inline-01".equals(host.name)) {
            vars.put("inline", Map.of("text", "foo"));
            vars.put(host, Collections.emptyMap());
        } else {
            vars.put(host, new HashMap<>());
            vars.put("web", Map.of("text", mgr.inventory.canDecrypt ? "hello" : "locked"));
        }
        return vars;
    }

    @Test
    void testVaultPasswordFile() {
        DummyInventoryManager mgr = new DummyInventoryManager("vault/inventory", false, new String[]{"vault/vaultpass"});
        DummyHost host = mgr.inventory.getHost("web-01");
        String group = mgr.inventory.getGroup("web");
        Map<Object, Map<String, Object>> vars = tidyAllTheVariables(host, mgr);
        assertEquals("hello", vars.get(group).get("text"));
    }

    @Test
    void testVaultPasswordFiles() {
        DummyInventoryManager mgr = new DummyInventoryManager("vault/inventory", false, new String[]{"vault/vaultpass", "vault/notthevaultpass"});
        DummyHost host = mgr.inventory.getHost("web-01");
        String group = mgr.inventory.getGroup("web");
        Map<Object, Map<String, Object>> vars = tidyAllTheVariables(host, mgr);
        assertEquals("hello", vars.get(group).get("text"));
    }

    @Test
    void testVaultIds() {
        DummyInventoryManager mgr = new DummyInventoryManager("vault_ids/inventory", false, new String[]{}, new String[]{"another_vault@vault_ids/vaultpass"});
        DummyHost host = mgr.inventory.getHost("web-01");
        Map<Object, Map<String, Object>> vars = tidyAllTheVariables(host, mgr);
        assertEquals("world", vars.get(host).get("hello"));
    }

    @Test
    void testNoVaultPass() {
        DummyInventoryManager mgr = new DummyInventoryManager("vault/inventory", false, new String[]{});
        DummyHost host = mgr.inventory.getHost("web-01");
        Map<Object, Map<String, Object>> vars = tidyAllTheVariables(host, mgr);
        assertNotEquals("hello", vars.get("web").get("text"));
    }

    @Test
    void testInlineVaultWithoutPassword() {
        DummyInventoryManager mgr = new DummyInventoryManager("vault/inventory", false, new String[]{});
        DummyHost host = mgr.inventory.getHost("inline-01");
        String group = mgr.inventory.getGroup("inline");
        Map<Object, Map<String, Object>> vars = tidyAllTheVariables(host, mgr);
        assertTrue(vars.get(group).containsKey("text"));
        assertTrue(!vars.get(host).containsKey("text"));
    }
}