package com.initstring.original;

import com.initstring.linkedin2username.NameMutator;
import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

public class TestNamemutatorTable {

    static class NamePair {
        String input;
        Map<String, String> dict;
        NamePair(String i, Map<String, String> d) { input = i; dict = d; }
    }

    @Test
    public void testCleanAndSplitName() {
        List<NamePair> testCases = Arrays.asList(
            new NamePair("John Smith", Map.of("first", "john", "second", "smith")),
            new NamePair("Jane D'oe", Map.of("first", "jane", "second", "doe")),
            new NamePair("Dr. Ángela Gómez (MBA, PhD)", Map.of("first", "angela", "second", "gomez")),
            new NamePair("Mr. François Noël", Map.of("first", "francois", "second", "noel")),
            new NamePair("José Niño", Map.of("first", "jose", "second", "nino")),
            new NamePair("Joe (CTO) Bloggs", Map.of("first", "joe", "second", "bloggs")),
            new NamePair("Alíce O'Conñor (CISO)", Map.of("first", "alice", "second", "oconor")),
            new NamePair("Mononym", Map.of("first", "mononym", "second", ""))
        );
        for (NamePair t : testCases) {
            NameMutator nm = new NameMutator(t.input);
            // Assuming the NameMutator exposes its 'name' map directly as in python.
            // Otherwise, adapt to the correct method or getter.
            assertEquals(t.dict, nm.getNameMap());
        }
    }

    @Test
    public void testFirst() {
        List<Map.Entry<String,String>> testCases = Arrays.asList(
            Map.entry("John Smith", "john"),
            Map.entry(" Jane Smith ", "jane"),
            Map.entry("Dr. Ángela Gómez (MBA, PhD)", "angela"),
            Map.entry("Mononym", "mononym"),
            Map.entry("", "")
        );
        for (Map.Entry<String,String> tc : testCases) {
            NameMutator nm = new NameMutator(tc.getKey());
            assertEquals(Set.of(tc.getValue()), nm.first());
        }
    }

    @Test
    public void testLast() {
        List<Map.Entry<String,String>> testCases = Arrays.asList(
            Map.entry("John Smith", "smith"),
            Map.entry("Jane D'oe", "doe"),
            Map.entry("Dr. Ángela Gómez (MBA, PhD)", "gomez"),
            Map.entry("Mr. François Noël", "noel"),
            Map.entry("José Niño", "nino"),
            Map.entry("Joe (CTO) Bloggs", "bloggs"),
            Map.entry("Alíce O'Conñor (CISO)", "oconor"),
            Map.entry("Mononym", ""),
            Map.entry("", "")
        );
        for (Map.Entry<String,String> tc : testCases) {
            NameMutator nm = new NameMutator(tc.getKey());
            assertEquals(tc.getValue(), nm.last());
        }
    }

    @Test
    public void testMutatorsAllVariants() {
        NameMutator nm = new NameMutator("John O'Conner (CEO)");
        Set<String> variants = nm.mutators();
        assertTrue(variants.contains("johnoconner"));
        assertTrue(variants.contains("joconner"));
        assertTrue(variants.stream().anyMatch(v -> v.contains("john.o") || v.contains("johno")));
    }

    @Test
    public void testNameWithEmptyString() {
        NameMutator nm = new NameMutator("");
        assertEquals(Map.of("first", "", "second", ""), nm.getNameMap());
        assertEquals(Set.of(), nm.mutators());
    }
}