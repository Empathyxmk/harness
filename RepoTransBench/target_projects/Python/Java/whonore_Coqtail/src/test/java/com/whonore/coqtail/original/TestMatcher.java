package com.whonore.coqtail.original;

import org.junit.jupiter.api.Test;
import com.whonore.coqtail.matcher.Matcher;
import static org.junit.jupiter.api.Assertions.*;

public class TestMatcher {

    @Test
    void testMatchTokensDiff() {
        Matcher matcher = new Matcher();
        String[] pat = { "cat", "dog" };
        String[] text = { "cat", "bird" };
        assertFalse(matcher.matchTokens(pat, text));
    }

    @Test
    void testMatchTokensContained() {
        Matcher matcher = new Matcher();
        String[] pat = { "tree", "leaf" };
        String[] text = { "tree", "root", "leaf" };
        // By the stub, but stub only matches length equality so will be false.
        boolean result = matcher.matchTokens(pat, text);
        // Depending on the stub design, this would be false. Adjust if needed.
        assertFalse(result);
    }

    @Test
    void testMatchTokensSuccess() {
        Matcher matcher = new Matcher();
        String[] pat = { "sun", "light" };
        String[] text = { "sun", "light" };
        assertTrue(matcher.matchTokens(pat, text));
    }

    @Test
    void testMatchTokensTooLong() {
        Matcher matcher = new Matcher();
        String[] pat = { "alpha", "beta", "gamma" };
        String[] text = { "alpha", "beta", "gamma", "delta" };
        assertFalse(matcher.matchTokens(pat, text));
    }

    @Test
    void testMatchTokensEmptyPattern() {
        Matcher matcher = new Matcher();
        String[] pat = {};
        String[] text = { "x", "y", "z" };
        assertTrue(matcher.matchTokens(pat, text));
    }
}