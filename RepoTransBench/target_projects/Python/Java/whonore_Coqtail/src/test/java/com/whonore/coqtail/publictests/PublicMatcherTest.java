package com.whonore.coqtail.publictests;

import org.junit.jupiter.api.Test;
import com.whonore.coqtail.matcher.Matcher;
import static org.junit.jupiter.api.Assertions.*;

public class PublicMatcherTest {

    @Test
    void testPublicMatchTokensDiff() {
        Matcher matcher = new Matcher();
        String[] pat = { "cat", "dog" };
        String[] text = { "cat", "bird" };
        assertFalse(matcher.matchTokens(pat, text));
    }

    @Test
    void testPublicMatchTokensContained() {
        Matcher matcher = new Matcher();
        String[] pat = { "tree", "leaf" };
        String[] text = { "tree", "root", "leaf" };
        boolean output = matcher.matchTokens(pat, text);
        // Stub implementation returns false as pattern length does not match input length.
        assertFalse(output);
    }

    @Test
    void testPublicMatchTokensSuccess() {
        Matcher matcher = new Matcher();
        String[] pat = { "sun", "light" };
        String[] text = { "sun", "light" };
        assertTrue(matcher.matchTokens(pat, text));
    }

    @Test
    void testPublicMatchTokensTooLong() {
        Matcher matcher = new Matcher();
        String[] pat = { "alpha", "beta", "gamma" };
        String[] text = { "alpha", "beta", "gamma", "delta" };
        boolean output = matcher.matchTokens(pat, text);
        assertFalse(output);
    }

    @Test
    void testPublicMatchTokensEmptyPattern() {
        Matcher matcher = new Matcher();
        String[] pat = {};
        String[] text = { "x", "y", "z" };
        assertTrue(matcher.matchTokens(pat, text));
    }
}