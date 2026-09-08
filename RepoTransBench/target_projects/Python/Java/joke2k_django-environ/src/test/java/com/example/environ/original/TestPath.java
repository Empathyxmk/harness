package com.example.environ.original;

import org.junit.jupiter.api.Test;
import java.nio.file.Paths;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Translated from: tests/test_path.py
 * This assumes PathUtil is a utility class that wraps java.nio.Path.
 */
public class TestPath {

    @Test
    void testPathJoin() {
        PathUtil p = new PathUtil("/a/b");
        assertEquals(Paths.get("/a/b/c").normalize(), p.join("c").toPath().normalize());
    }

    @Test
    void testAncestors() {
        PathUtil p = new PathUtil("/tmp/foo/bar");
        assertEquals(Paths.get("/tmp/foo"), p.parent().toPath());
        assertEquals(Paths.get("/tmp"), p.parent().parent().toPath());
        assertEquals(Paths.get("/"), p.parent().parent().parent().toPath());
    }

    @Test
    void testStringToPath() {
        PathUtil p = new PathUtil("/usr/local/bin");
        assertEquals("/usr/local/bin", p.toString());
    }
}