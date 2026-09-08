package com.oxsecurity.maskerlogger.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import com.oxsecurity.maskerlogger.ahocorasickregexmatch.RegexMatcher;

public class TestAhoCorasickRegexMatch {

    @Test
    public void testFindMatchesAndMask() {
        RegexMatcher matcher = new RegexMatcher(null, 90);
        String msg = "password: hunter2";
        // Simulate find_matches, mask
        boolean matches = matcher.findMatches(msg).length > 0;
        assertTrue(matches);
        String masked = matcher.mask(msg);
        assertTrue(masked.contains("***"));
    }

    @Test
    public void testParseConfigFailure() {
        RegexMatcher matcher = new RegexMatcher("nonexistent_path.toml", 80);
        String out = matcher.mask("password: hunter2 super");
        assertTrue(out.contains("*"));
    }
}