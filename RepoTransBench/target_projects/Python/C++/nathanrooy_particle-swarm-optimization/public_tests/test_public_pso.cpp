#include <gtest/gtest.h>
#include "pso/pso_simple.h"
#include "pso/cost_functions.h"
#include <vector>

TEST(MinimizeTestPublic, WithSphereFunctionPublic) {
    std::vector<double> x0{-2.0, 3.0};
    std::vector<std::pair<double, double>> bounds{{-10.0, 10.0}, {-10.0, 10.0}};
    auto result = pso::minimize(pso::sphere, x0, bounds, 5, 12, false);
    EXPECT_LE(result.first, pso::sphere(x0));
    EXPECT_EQ(result.second.size(), x0.size());
}