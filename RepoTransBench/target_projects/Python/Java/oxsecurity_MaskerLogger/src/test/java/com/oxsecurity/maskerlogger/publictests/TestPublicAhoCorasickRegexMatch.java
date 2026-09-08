package com.oxsecurity.maskerlogger.publictests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.util.Arrays;
import java.util.List;

import com.oxsecurity.maskerlogger.ahocorasickregexmatch.AhoCorasick;
import com.oxsecurity.maskerlogger.ahocorasickregexmatch.RegexMatcher;

public class TestPublicAhoCorasickRegexMatch {

    @Test
    public void testBuildTrieAndMatch() {
        List<String> keys = Arrays.asList("bear", "wolf", "lion");
        AhoCorasick trie = AhoCorasick.build(keys);
        List<String> found = trie.iter("the wolf and lion bear witness");
        assertTrue(found.contains("wolf"));
        assertTrue(found.contains("lion"));
        assertTrue(found.contains("bear"));
        assertEquals(3, found.size());
    }

    @Test
    public void testBuildRegexFromConfig() {
        RegexMatcher rm = new RegexMatcher();
        Object result = rm.loadRegexesFromConfig();
        assertTrue(result instanceof java.util.List);
    }
}