package com.github.davidmoten.geo;

import static org.junit.Assert.*;

import org.junit.Test;

import java.util.Collections;
import java.util.HashSet;
import java.util.Set;
import java.util.TreeSet;

public class CoverageTest {

    @Test
    public void testGetHashesReturnsSameSet() {
        Set<String> h = new HashSet<>();
        h.add("abc123");
        Coverage c = new Coverage(h, 2.5);
        assertEquals(h, c.getHashes());
    }

    @Test
    public void testGetRatio() {
        Set<String> h = new HashSet<>();
        h.add("abc123");
        Coverage c = new Coverage(h, 2.7);
        assertEquals(2.7, c.getRatio(), 0.0);
    }

    @Test
    public void testGetHashLengthWithEmptySet() {
        Coverage c = new Coverage(Collections.emptySet(), 1);
        assertEquals(0, c.getHashLength());
    }

    @Test
    public void testGetHashLengthWithNonEmptySet() {
        Set<String> set = new TreeSet<>();
        set.add("aaaa");
        Coverage c = new Coverage(set, 1.1);
        assertEquals(4, c.getHashLength());
    }

    @Test
    public void testToString() {
        Set<String> hashes = new TreeSet<>();
        hashes.add("hash1");
        Coverage c = new Coverage(hashes, 3.14);
        String s = c.toString();
        assertTrue(s.contains("hashes"));
        assertTrue(s.contains("ratio"));
    }
}