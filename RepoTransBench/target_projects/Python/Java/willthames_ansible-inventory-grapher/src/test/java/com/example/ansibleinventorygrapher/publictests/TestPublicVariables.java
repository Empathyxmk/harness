package com.example.ansibleinventorygrapher.publictests;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

import java.util.*;

class TestPublicVariables {

    @Test
    void testPublicBasicVarStrip() {
        Map<String,Integer> d = new HashMap<>();
        d.put("public_private", 123);
        d.put("should_keep", 456);
        Map<String,Integer> result = new HashMap<>();
        for (Map.Entry<String,Integer> e : d.entrySet()) {
            if (!e.getKey().startsWith("public_"))
                result.put(e.getKey(), e.getValue());
        }
        assertTrue(result.containsKey("should_keep"));
        assertFalse(result.containsKey("public_private"));
    }

    @Test
    void testPublicGroupVarPrecedence() {
        Map<String,String> groupVars = Map.of("pubkey", "groupval", "shared", "gshared");
        Map<String,String> hostVars = Map.of("pubkey", "hostval", "override", "hval", "shared", "hshared");
        Map<String,String> mergedVars = new HashMap<>(groupVars);
        mergedVars.putAll(hostVars);
        assertEquals("hostval", mergedVars.get("pubkey"));
        assertEquals("hshared", mergedVars.get("shared"));
        assertEquals("hval", mergedVars.get("override"));
        // No actual value "groupval" expected after merge
        assertFalse(mergedVars.containsValue("groupval"));
    }

    @Test
    void testPublicNestedVars() {
        Map<String,Object> hostVars = new HashMap<>();
        Map<String,Object> nested = new HashMap<>();
        nested.put("public_hidden", "value");
        nested.put("visible", 42);
        hostVars.put("outer", nested);
        hostVars.put("plain", 10);

        Map<String, Object> result = cleanVars(hostVars);

        assertTrue(result.containsKey("plain"));
        assertTrue(result.containsKey("outer"));
        Map<String,Object> outer = (Map<String,Object>) result.get("outer");
        assertFalse(outer.containsKey("public_hidden"));
        assertTrue(outer.containsKey("visible"));
    }

    static Map<String, Object> cleanVars(Map<String, Object> varsDict) {
        Map<String, Object> cleaned = new HashMap<>();
        for (Map.Entry<String, Object> e : varsDict.entrySet()) {
            String k = e.getKey();
            Object v = e.getValue();
            if (v instanceof Map) {
                Map<?,?> mapv = (Map<?,?>) v;
                Map<String,Object> cleanedInner = new HashMap<>();
                for (Map.Entry<?,?> ine : mapv.entrySet()) {
                    String ik = ine.getKey().toString();
                    if (!ik.startsWith("public_"))
                        cleanedInner.put(ik, ine.getValue());
                }
                cleaned.put(k, cleanedInner);
            } else if (!k.startsWith("public_")) {
                cleaned.put(k, v);
            }
        }
        return cleaned;
    }
}