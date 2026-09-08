#include <gtest/gtest.h>
#include "optimizer.h"

TEST(Optimizer, Selector_ValidAlgorithm) {
    std::vector<double> func_details = {/* F1 settings */};
    int popSize = 5;
    int Iter = 2;
    auto algo = selector("SSA", func_details, popSize, Iter);
    // Check solution object for "fitness" or "convergence" attribute
    EXPECT_TRUE(algo.has_fitness() || algo.has_convergence());
}

TEST(Optimizer, Selector_InvalidAlgorithm) {
    std::vector<double> func_details = {/* F1 settings */};
    auto result = selector("DoesNotExist", func_details, 5, 2);
    EXPECT_TRUE(result.is_none() || !result);
}