#include <gtest/gtest.h>
#include "optimizers/PSO.h"

TEST(PSO, RunsAndOutputsValid) {
    auto objective_function = [](const std::vector<double>& x) {
        double s = 0;
        for (double v : x) s += v * v;
        return s;
    };
    std::vector<double> lb(5, -10);
    std::vector<double> ub(5, 10);
    int dims = 5, PopSize = 10, iters = 30;
    Solution sol = PSO(objective_function, lb, ub, dims, PopSize, iters);
    EXPECT_EQ(sol.bestIndividual.size(), dims);
    EXPECT_EQ(sol.convergence.size(), iters);
    EXPECT_GE(sol.best, 0.0);
}