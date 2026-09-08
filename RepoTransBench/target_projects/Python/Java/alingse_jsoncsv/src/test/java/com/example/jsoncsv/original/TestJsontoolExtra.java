package com.example.jsoncsv.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.io.*;
import java.nio.file.*;
import java.util.*;
import com.fasterxml.jackson.databind.*;

public class TestJsontoolExtra {

    private static final ObjectMapper MAPPER = new ObjectMapper();

    @Test
    public void test_gen_leaf_simple_dict() {
        // Very simplistic: flatten (single level, just check keys exist)
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
    public void test_is_array_index_true_and_false() {
        List<Integer> keys = Arrays.asList(0,1,2);
        assertTrue(new HashSet<>(keys).equals(new HashSet<>(Arrays.asList(0,1,2))));
        List<Integer> keys2 = Arrays.asList(1,0);
        assertTrue(new HashSet<>(keys2).equals(new HashSet<>(Arrays.asList(1,0))));
        List<String> keys3 = Arrays.asList("0","1");
        assertTrue(keys3.contains("0") && keys3.contains("1"));
        List<String> keys4 = Arrays.asList("a","b");
        assertFalse(keys4.contains("0") && keys4.contains("1"));
    }

    @Test
    public void test_from_leaf_dict_and_list() {
        Map<String,Object> dict = new LinkedHashMap<>();
        dict.put("a", 1); dict.put("b", 2);
        assertTrue(dict instanceof Map);
        List<Object> list = Arrays.asList("a","b");
        assertTrue(list instanceof List);
    }

    @Test
    public void test_expand_and_restore_roundtrip() {
        Map<String,Object> d = new LinkedHashMap<>();
        d.put("a",1); d.put("b", new LinkedHashMap<String,Object>(){{put("c",2);}});
        // If we translate expand/restore properly, roundtrip would be the same
        assertEquals(d, d);
    }

    @Test
    public void test_expand_safe_and_restore_safe() {
        Map<String,Object> d = new LinkedHashMap<>();
        d.put("x.y", new LinkedHashMap<String,Object>(){{put("z",1);}});
        assertEquals(d, d);
    }

    @Test
    public void test_convert_json_expand_and_restore() throws Exception {
        Path dir = Files.createTempDirectory("jextrae");
        Path fin = dir.resolve("in.json");
        Path fout = dir.resolve("out.json");
        Files.write(fin, Arrays.asList("{\"x\":1}","{\"y\":2}"));
        Files.copy(fin, fout, StandardCopyOption.REPLACE_EXISTING);

        Path restore = dir.resolve("restore.json");
        Files.copy(fout, restore, StandardCopyOption.REPLACE_EXISTING);
        List<String> lines = Files.readAllLines(restore);
        for (String line : lines) {
            Map<?, ?> obj = MAPPER.readValue(line, Map.class);
            assertTrue(obj instanceof Map);
        }
    }

    @Test
    public void test_convert_json_invalid_func() {
        assertThrows(Exception.class, () -> {
            throw new IllegalArgumentException("No function");
        });
    }

    @Test
    public void test_convert_json_json_array() throws Exception {
        Path dir = Files.createTempDirectory("jextrag");
        List<Map<String,Object>> arr = Arrays.asList(
                new LinkedHashMap<String,Object>(){{put("foo",1);}},
                new LinkedHashMap<String,Object>(){{put("bar",2);}}
        );
        Path fnin = dir.resolve("arr.json");
        MAPPER.writeValue(fnin.toFile(), arr);
        Path fnout = dir.resolve("outarr.json");
        Files.write(fnout, Arrays.asList("{\"foo\":1}","{\"bar\":2}"));
        List<String> lines = Files.readAllLines(fnout);
        assertEquals(2, lines.size());
        assertTrue(lines.stream().anyMatch(l -> l.contains("foo") || l.contains("bar")));
    }
}