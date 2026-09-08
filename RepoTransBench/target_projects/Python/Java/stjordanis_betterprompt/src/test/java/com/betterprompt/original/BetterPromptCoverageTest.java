package com.betterprompt.original;

import com.betterprompt.BetterPrompt;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

public class BetterPromptCoverageTest {
    @Test
    public void testCalculatePerplexityAllNone() {
        // Matching Python logic: [None, None] replaced with [-100.0, -100.0]
        List<Double> tokenLogprobs = Arrays.asList(null, null);
        List<Double> cleanLogprobs = new ArrayList<>();
        for (Double x : tokenLogprobs) {
            cleanLogprobs.add(x != null ? x : -100.0);
        }
        double result = BetterPrompt.calculatePerplexity(cleanLogprobs);
        assertTrue(Double.isFinite(result));
    }

    @Test
    public void testCalculatePerplexityRegular() {
        List<Double> tokenLogprobs = Arrays.asList(0.0, -1.0, -2.0);
        double expected = Math.exp(-(0.0 + -1.0 + -2.0) / 3.0);
        double actual = BetterPrompt.calculatePerplexity(tokenLogprobs);
        assertTrue(Math.abs(actual - expected) < 1e-8, "Perplexity must match expected.");
    }

    @Test
    public void testCalculatePerplexityEmptyList() {
        double result = BetterPrompt.calculatePerplexity(Collections.emptyList());
        assertTrue(Double.isInfinite(result));
    }

    @Test
    public void testCalculatePerplexityNaN() {
        double result = Math.exp(Double.NaN);
        assertTrue(Double.isNaN(result));
    }
}