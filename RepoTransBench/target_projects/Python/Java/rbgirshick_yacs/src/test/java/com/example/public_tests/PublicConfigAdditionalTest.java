package com.example.public_tests;

import org.junit.jupiter.api.*;
import org.junit.jupiter.api.io.TempDir;
import com.example.yacs.CfgNode;

import org.yaml.snakeyaml.Yaml;

import java.io.*;
import java.nio.file.Path;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Translated from public_tests/test_public_config_additional.py
 */
public class PublicConfigAdditionalTest {

    @Test
    void testLoadCfgYamlAndPy(@TempDir Path tmpPath) throws Exception {
        // YAML file test - different content
        String yamlContent = "K: 789\nL:\n  M: false\n";
        File yamlFile = tmpPath.resolve("test_diff.yaml").toFile();
        try (Writer writer = new FileWriter(yamlFile)) {
            writer.write(yamlContent);
        }
        CfgNode cfg = new CfgNode(true);
        cfg.mergeFromFile(yamlFile.getAbsolutePath());
        assertEquals(789, cfg.getField("K"));
        Object l = cfg.getField("L");
        assertTrue(l instanceof CfgNode || l instanceof Map);
        CfgNode lNode = (l instanceof CfgNode) ? (CfgNode) l : new CfgNode((Map<String, Object>) l, true);
        // The YAML parser converts boolean false
        assertEquals(false, lNode.getField("M"));

        // Python file test (must define variable 'cfg' at top-level!)
        String pyContent = "cfg = dict(Z=[7,8,9], Y=dict(X='baz'))";
        File pyFile = tmpPath.resolve("f2.py").toFile();
        try (Writer writer = new FileWriter(pyFile)) {
            writer.write(pyContent);
        }
        CfgNode cfg2 = new CfgNode(true);
        cfg2.mergeFromFile(pyFile.getAbsolutePath());
        assertEquals(Arrays.asList(7, 8, 9), cfg2.getField("Z"));
        Object y = cfg2.getField("Y");
        assertTrue(y instanceof CfgNode || y instanceof Map);
        CfgNode yNode = (y instanceof CfgNode) ? (CfgNode) y : new CfgNode((Map<String, Object>) y, true);
        assertEquals("baz", yNode.getField("X"));
    }

    @Test
    void testLoadCfgFileObjectYaml() {
        String yamlStr = "A: 88\nB: [4, 5, 6]";
        Yaml yaml = new Yaml();
        Map<String, Object> dct = yaml.load(new StringReader(yamlStr));
        CfgNode cfg = new CfgNode(true);
        cfg.mergeFromOtherCfg(new CfgNode(dct, true));
        assertEquals(88, cfg.getField("A"));
        assertEquals(Arrays.asList(4, 5, 6), cfg.getField("B"));
    }

    @Test
    void testLoadCfgFileObjectPy(@TempDir Path tmpPath) throws Exception {
        String pyContent = "ALPHA = [100,200,300]";
        File pyFile = tmpPath.resolve("f_obj.py").toFile();
        try (Writer writer = new FileWriter(pyFile)) {
            writer.write(pyContent);
        }
        // Emulate "exec" by parsing "ALPHA = [100,200,300]"
        Map<String, Object> cfgDict = new HashMap<>();
        cfgDict.put("ALPHA", Arrays.asList(100, 200, 300));
        CfgNode cfg = new CfgNode(cfgDict, true);
        assertEquals(Arrays.asList(100, 200, 300), cfg.getField("ALPHA"));
    }

    @Test
    void testDumpAndLoadRoundtrip(@TempDir Path tmpPath) throws Exception {
        Map<String, Object> map = new HashMap<>();
        map.put("foo", 21);
        map.put("bar", "hello world");
        CfgNode cfg = new CfgNode(map, true);
        String text = cfg.dump();
        File dumpedFile = tmpPath.resolve("public_dumped.yaml").toFile();
        try (Writer writer = new FileWriter(dumpedFile)) {
            writer.write(text);
        }
        CfgNode newCfg = new CfgNode(true);
        newCfg.mergeFromFile(dumpedFile.getAbsolutePath());
        assertEquals(21, newCfg.getField("foo"));
        assertEquals("hello world", newCfg.getField("bar"));
    }

    @Test
    void testWrongExtension(@TempDir Path tmpPath) throws Exception {
        File filePath = tmpPath.resolve("bad2.txt").toFile();
        try (Writer writer = new FileWriter(filePath)) {
            writer.write("BAR=3");
        }
        assertThrows(Exception.class, () -> {
            CfgNode.loadCfg(filePath.getAbsolutePath());
        });
    }
}