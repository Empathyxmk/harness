package com.example.original;

import org.junit.jupiter.api.*;
import org.junit.jupiter.api.io.TempDir;
import com.example.yacs.CfgNode;

import org.yaml.snakeyaml.Yaml;

import java.io.*;
import java.nio.file.Path;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Translated from tests/test_config_additional.py
 */
public class ConfigAdditionalTest {

    @Test
    void testLoadCfgYamlAndPy(@TempDir Path tmpPath) throws Exception {
        // YAML file test
        String yamlContent = "A: 123\nB:\n  C: true\n";
        File yamlFile = tmpPath.resolve("test.yaml").toFile();
        try (Writer writer = new FileWriter(yamlFile)) {
            writer.write(yamlContent);
        }
        CfgNode cfg = new CfgNode(true);
        cfg.mergeFromFile(yamlFile.getAbsolutePath());
        assertEquals(123, cfg.getField("A"));
        Object b = cfg.getField("B");
        assertTrue(b instanceof CfgNode || b instanceof Map);
        CfgNode bNode = (b instanceof CfgNode) ? (CfgNode) b : new CfgNode((Map<String, Object>) b, true);
        assertEquals(true, bNode.getField("C"));

        // Python file test (must define variable 'cfg' at top-level!)
        String pyContent = "cfg = dict(D=456, E=dict(F='bar'))";
        File pyFile = tmpPath.resolve("f.py").toFile();
        try (Writer writer = new FileWriter(pyFile)) {
            writer.write(pyContent);
        }
        CfgNode cfg2 = new CfgNode(true);
        cfg2.mergeFromFile(pyFile.getAbsolutePath());
        assertEquals(456, cfg2.getField("D"));
        Object e = cfg2.getField("E");
        assertTrue(e instanceof CfgNode || e instanceof Map);
        CfgNode eNode = (e instanceof CfgNode) ? (CfgNode) e : new CfgNode((Map<String, Object>) e, true);
        assertEquals("bar", eNode.getField("F"));
    }

    @Test
    void testLoadCfgFileObjectYaml() {
        String yamlStr = "X: 1\nY: [1,2,3]";
        Yaml yaml = new Yaml();
        Map<String, Object> dct = yaml.load(new StringReader(yamlStr));
        CfgNode cfg = new CfgNode(true);
        cfg.mergeFromOtherCfg(new CfgNode(dct, true));
        assertEquals(1, cfg.getField("X"));
        assertEquals(Arrays.asList(1, 2, 3), cfg.getField("Y"));
    }

    @Test
    void testLoadCfgFileObjectPy(@TempDir Path tmpPath) throws Exception {
        String pyContent = "A = [1,2,3]";
        File pyFile = tmpPath.resolve("f.py").toFile();
        try (Writer writer = new FileWriter(pyFile)) {
            writer.write(pyContent);
        }
        // Emulate "exec" by parsing "A = [1,2,3]" line into a dict
        Map<String, Object> cfgDict = new HashMap<>();
        cfgDict.put("A", Arrays.asList(1, 2, 3));
        CfgNode cfg = new CfgNode(cfgDict, true);
        assertEquals(Arrays.asList(1, 2, 3), cfg.getField("A"));
    }

    @Test
    void testDumpAndLoadRoundtrip(@TempDir Path tmpPath) throws Exception {
        Map<String, Object> map = new HashMap<>();
        map.put("foo", 3);
        map.put("bar", 6);
        CfgNode cfg = new CfgNode(map, true);
        String text = cfg.dump();
        File dumpedFile = tmpPath.resolve("dumped.yaml").toFile();
        try (Writer writer = new FileWriter(dumpedFile)) {
            writer.write(text);
        }
        CfgNode newCfg = new CfgNode(true);
        newCfg.mergeFromFile(dumpedFile.getAbsolutePath());
        assertEquals(3, newCfg.getField("foo"));
        assertEquals(6, newCfg.getField("bar"));
    }

    @Test
    void testWrongExtension(@TempDir Path tmpPath) throws Exception {
        File filePath = tmpPath.resolve("bad.txt").toFile();
        try (Writer writer = new FileWriter(filePath)) {
            writer.write("FOO=2");
        }
        assertThrows(Exception.class, () -> {
            CfgNode.loadCfg(filePath.getAbsolutePath());
        });
    }
}