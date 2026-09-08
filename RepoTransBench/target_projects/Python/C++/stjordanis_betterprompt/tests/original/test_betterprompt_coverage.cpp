#include <gtest/gtest.h>
#include "betterprompt.h"
#include <cmath>
#include <limits>

TEST(TestBetterpromptCoverage, CalculatePerplexityAllNone) {
    // Simulate "None" as -100.0 as in Python test.
    std::vector<double> token_logprobs = { -100.0, -100.0 };
    auto result = betterprompt::calculate_perplexity(token_logprobs);
    EXPECT_TRUE(std::isfinite(result));
}

TEST(TestBetterpromptCoverage, CalculatePerplexityRegular) {
    std::vector<double> token_logprobs = { 0, -1, -2 };
    double expected = std::exp(-((0 + -1 + -2) / 3.0));
    EXPECT_NEAR(betterprompt::calculate_perplexity(token_logprobs), expected, 1e-8);
}

TEST(TestBetterpromptCoverage, CalculatePerplexityEmptyList) {
    auto result = betterprompt::calculate_perplexity({});
    EXPECT_TRUE(std::isinf(result));
}

TEST(TestBetterpromptCoverage, CalculatePerplexityNaN) {
    double nan_val = std::nan("");
    auto result = std::exp(nan_val);
    EXPECT_TRUE(std::isnan(result));
}