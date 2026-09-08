#include <gtest/gtest.h>
#include "pso/cost_functions.h"
#include <vector>

TEST(SphereTestPublic, AllZerosPublic) {
    std::vector<double> x{0, 0, 0, 0};
    EXPECT_DOUBLE_EQ(pso::sphere(x), 0.0);
}

TEST(SphereTestPublic, SingleValuePublic) {
    std::vector<double> x{4};
    EXPECT_DOUBLE_EQ(pso::sphere(x), 16.0);
}

TEST(SphereTestPublic, NegativeValuesPublic) {
    std::vector<double> x{-3, -2};
    EXPECT_DOUBLE_EQ(pso::sphere(x), 9.0 + 4.0);
}

TEST(SphereTestPublic, MixedValuesPublic) {
    std::vector<double> x{2, -3, 4};
    EXPECT_DOUBLE_EQ(pso::sphere(x), 4.0 + 9.0 + 16.0);
}

TEST(SphereTestPublic, EmptyPublic) {
    std::vector<double> x;
    EXPECT_DOUBLE_EQ(pso::sphere(x), 0.0);
}

TEST(SphereTestPublic, MainGuardDoesNothingPublic) {
    EXPECT_TRUE(true);
}