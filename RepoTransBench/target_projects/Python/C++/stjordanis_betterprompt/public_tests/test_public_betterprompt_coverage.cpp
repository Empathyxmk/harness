#include <gtest/gtest.h>
#include "betterprompt.h"
#include <cmath>
#include <limits>

TEST(TestPublicBetterpromptCoverage, CalculatePerplexityAllZeroes) {
    std::vector<double> token_logprobs = {0, 0, 0};
    double result = betterprompt::calculate_perplexity(token_logprobs);
    EXPECT_NEAR(result, 1.0, 1e-8);
}

TEST(TestPublicBetterpromptCoverage, CalculatePerplexityPositiveAndNegative) {
    std::vector<double> token_logprobs = {1, -1, -2, 2};
    double expected = std::exp(-( (1+-1+-2+2) / 4.0 ));
    EXPECT_NEAR(betterprompt::calculate_perplexity(token_logprobs), expected, 1e-8);
}

TEST(TestPublicBetterpromptCoverage, CalculatePerplexityEmptyList) {
    auto result = betterprompt::calculate_perplexity({});
    EXPECT_TRUE(std::isinf(result));
}

TEST(TestPublicBetterpromptCoverage, CalculatePerplexityLarge) {
    std::vector<double> token_logprobs = {10, 12, 15};
    double expected = std::exp(-( (10+12+15) / 3.0 ));
    EXPECT_NEAR(betterprompt::calculate_perplexity(token_logprobs), expected, 1e-8);
}