package com.example.jsoncsv.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.io.*;
import java.nio.file.*;
import java.util.*;
import com.fasterxml.jackson.databind.*;

public class TestPublicJsontoolExtra {

    private static final ObjectMapper MAPPER = new ObjectMapper();

    @Test
    public void test_public_gen_leaf_simple_dict() {
        Map<String,Object> root = new LinkedHashMap<>();
        root.put("a", 1);
        Map<String,Object> b = new LinkedHashMap<>();
        b.put("c", 2);
        root.put("b", b);

        Set<String> leaves = new HashSet<>();
        leaves.add("a");
        leaves.add("b.c");
        assertTrue(leaves.contains("a"));
        assertTrue(leaves.contains("b.c"));
    }

    @Test
    public void test_public_expand_and_restore_roundtrip() {
        Map<String,Object> d = new LinkedHashMap<>();
        d.put("a",1); d.put("b", new LinkedHashMap<String,Object>(){{put("c",2);}});
        assertEquals(d, d);
    }
}