package com.peritus.bumpversion.publictests;

import org.junit.jupiter.api.Test;

import java.util.Map;
import java.util.function.Supplier;

import static org.junit.jupiter.api.Assertions.*;

class PublicInitVcsTest {

    @Test
    void testKnownVcsMappingsNonGitMercurial() {
        Map<String, Supplier<Object>> vcsMap = KnownVcsMap.getVcsMap();
        assertTrue(vcsMap.containsKey("hg"));
        assertTrue(vcsMap.containsKey("svn"));
    }

    @Test
    void testVcsMapContentTypes() {
        Map<String, Supplier<Object>> vcsMap = KnownVcsMap.getVcsMap();
        for (Map.Entry<String, Supplier<Object>> entry : vcsMap.entrySet()) {
            assertTrue(entry.getKey() instanceof String);
            assertNotNull(entry.getValue());
        }
    }

    @Test
    void testDefaultVcsScenarios() {
        Map<String, Supplier<Object>> vcsMap = KnownVcsMap.getVcsMap();
        assertTrue(vcsMap.containsKey("hg") || vcsMap.containsKey("svn"));
    }
}

// Dummy for known vcs mappings
class KnownVcsMap {
    public static Map<String, Supplier<Object>> getVcsMap() {
        return Map.of(
            "git", () -> new Object(),
            "hg", () -> new Object(),
            "svn", () -> new Object()
        );
    }
}