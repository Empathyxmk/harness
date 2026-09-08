#include <gtest/gtest.h>
#include "pso/pso_simple.h"
#include "pso/cost_functions.h"
#include <vector>

TEST(MinimizeTest, WithSphereFunction) {
    std::vector<double> x0{1.0, 2.0};
    std::vector<std::pair<double, double>> bounds{{-5.0, 5.0}, {-5.0, 5.0}};
    auto result = pso::minimize(pso::sphere, x0, bounds, 4, 15, false);
    EXPECT_LE(result.first, pso::sphere(x0));
    EXPECT_EQ(result.second.size(), x0.size());
}