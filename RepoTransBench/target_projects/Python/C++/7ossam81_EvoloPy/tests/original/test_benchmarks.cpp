#include <gtest/gtest.h>
#include <vector>
#include <cmath>
#include <algorithm>
#include <random>
#include "benchmarks.h"

// Example for prod
TEST(Benchmarks, Prod) {
    EXPECT_EQ(prod({1, 2, 3}), 6);
    EXPECT_EQ(prod({5, 5}), 25);
    EXPECT_EQ(prod({0, 1, 2, 3}), 0);
    EXPECT_EQ(prod({-1, 2, 3}), -6);
}

// Example for F1
TEST(Benchmarks, F1) {
    std::vector<double> x = {1, 2, 3};
    EXPECT_NEAR(F1(x), 14, 1e-6);
}

// ...continue all other function test cases as in the Python listing

// For np.allclose, you can implement as a helper
bool all_close(const std::vector<double>& a, const std::vector<double>& b, double tol=1e-6) {
    if (a.size() != b.size()) return false;
    for (size_t i = 0; i < a.size(); ++i)
        if (std::abs(a[i] - b[i]) > tol) return false;
    return true;
}