package com.oxsecurity.maskerlogger.publictests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import com.oxsecurity.maskerlogger.ahocorasickregexmatch.AhoCorasick;

import java.util.Collections;
import java.util.List;

public class TestPublicAhoCorasickRegexMatchAdditional {

    @Test
    public void testEmptyTrie() {
        AhoCorasick trie = AhoCorasick.build(Collections.emptyList());
        List<String> matches = trie.iter("this string has nothing of interest");
        assertEquals(0, matches.size());
    }

    @Test
    public void testPartialMatchNotFound() {
        AhoCorasick trie = AhoCorasick.build(java.util.Arrays.asList("dog", "cat", "mouse"));
        List<String> found = trie.iter("The quick brown fox.");
        assertEquals(0, found.size());
    }
}