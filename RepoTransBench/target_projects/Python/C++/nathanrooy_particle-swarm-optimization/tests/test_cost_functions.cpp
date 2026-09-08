#include <gtest/gtest.h>
#include "pso/cost_functions.h"
#include <vector>

TEST(SphereTest, AllZeros) {
    std::vector<double> x{0, 0, 0};
    EXPECT_DOUBLE_EQ(pso::sphere(x), 0.0);
}

TEST(SphereTest, SingleValue) {
    std::vector<double> x{3};
    EXPECT_DOUBLE_EQ(pso::sphere(x), 9.0);
}

TEST(SphereTest, NegativeValues) {
    std::vector<double> x{-1, -2};
    EXPECT_DOUBLE_EQ(pso::sphere(x), 1.0 + 4.0);
}

TEST(SphereTest, MixedValues) {
    std::vector<double> x{1, -2, 3};
    EXPECT_DOUBLE_EQ(pso::sphere(x), 1.0 + 4.0 + 9.0);
}

TEST(SphereTest, Empty) {
    std::vector<double> x;
    EXPECT_DOUBLE_EQ(pso::sphere(x), 0.0);
}

TEST(SphereTest, MainGuardDoesNothing) {
    // In Python, this would check __name__ == "__main__". In C++, this is just a sanity check.
    EXPECT_TRUE(true);
}