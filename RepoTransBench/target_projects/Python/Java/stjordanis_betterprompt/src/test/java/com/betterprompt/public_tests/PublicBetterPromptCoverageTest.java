package com.betterprompt.public_tests;

import com.betterprompt.BetterPrompt;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

public class PublicBetterPromptCoverageTest {
    @Test
    public void testPublicCalculatePerplexityAllZeroes() {
        List<Double> tokenLogprobs = Arrays.asList(0.0, 0.0, 0.0);
        double result = BetterPrompt.calculatePerplexity(tokenLogprobs);
        assertTrue(Math.abs(result - 1.0) < 1e-8);
    }

    @Test
    public void testPublicCalculatePerplexityPositiveAndNegative() {
        List<Double> tokenLogprobs = Arrays.asList(1.0, -1.0, -2.0, 2.0);
        double expected = Math.exp(-(1.0 + -1.0 + -2.0 + 2.0) / 4.0);
        double actual = BetterPrompt.calculatePerplexity(tokenLogprobs);
        assertTrue(Math.abs(actual - expected) < 1e-8);
    }

    @Test
    public void testPublicCalculatePerplexityEmptyList() {
        double result = BetterPrompt.calculatePerplexity(Collections.emptyList());
        assertTrue(Double.isInfinite(result));
    }

    @Test
    public void testPublicCalculatePerplexityLarge() {
        List<Double> tokenLogprobs = Arrays.asList(10.0, 12.0, 15.0);
        double expected = Math.exp(-(10.0 + 12.0 + 15.0) / 3.0);
        double actual = BetterPrompt.calculatePerplexity(tokenLogprobs);
        assertTrue(Math.abs(actual - expected) < 1e-8);
    }
}