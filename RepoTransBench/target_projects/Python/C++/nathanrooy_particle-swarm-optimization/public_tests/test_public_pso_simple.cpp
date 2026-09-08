#include <gtest/gtest.h>
#include "pso/pso_simple.h"
#include <vector>
#include <cmath>
#include <type_traits>

double public_cost(const std::vector<double>& x) {
    double sum = 0.0;
    for (auto val : x) sum += val * val;
    return sum + 1.0;
}

TEST(ParticleTestPublic, InstanceAndAttributesPublic) {
    std::vector<double> x0{7, -3, 2};
    pso::Particle p(x0);
    EXPECT_EQ(p.position_i.size(), x0.size());
    EXPECT_EQ(p.velocity_i.size(), x0.size());
    EXPECT_EQ(p.pos_best_i.size(), x0.size());
    EXPECT_NO_THROW(p.err_best_i);
    EXPECT_NO_THROW(p.err_i);
}

TEST(ParticleTestPublic, EvaluateAndPersonalBestPublic) {
    std::vector<double> x0{5, 6};
    pso::Particle p(x0);
    p.evaluate(public_cost);
    double err_first = p.err_best_i;
    p.position_i = {1, 2};
    p.evaluate(public_cost);
    EXPECT_TRUE(p.err_best_i == err_first || p.err_best_i == public_cost({1, 2}));
    EXPECT_DOUBLE_EQ(p.err_i, public_cost({1, 2}));
}

TEST(ParticleTestPublic, UpdateVelocityAndPositionPublic) {
    std::vector<double> x0{0.75, -0.25, 0.50};
    pso::Particle p(x0);
    p.pos_best_i = x0;
    std::vector<double> pos_best_g{0.0, 0.5, -0.5};
    auto old_v = p.velocity_i;
    p.update_velocity(pos_best_g);
    EXPECT_EQ(p.velocity_i.size(), old_v.size());

    std::vector<std::pair<double, double>> bounds{{-2, 2}, {-2, 2}, {-2, 2}};
    p.velocity_i = {3, -3, 4};
    p.update_position(bounds);
    for (double v : p.position_i) {
        EXPECT_LE(v, 2.0);
        EXPECT_GE(v, -2.0);
    }
}

TEST(MinimizeTestPublic, BasicPublic) {
    std::vector<double> x0{2, -3, 1};
    std::vector<std::pair<double, double>> bounds{{-7, 7}, {-7, 7}, {-7, 7}};
    auto result = pso::minimize(public_cost, x0, bounds, 4, 8, false);
    EXPECT_TRUE((std::is_same<decltype(result.first), double>::value));
    EXPECT_EQ(result.second.size(), x0.size());
}

TEST(MinimizeTestPublic, VerboseOutputPublic) {
    std::vector<double> x0{-1, 1};
    std::vector<std::pair<double, double>> bounds{{-2, 2}, {-2, 2}};
    auto result = pso::minimize(public_cost, x0, bounds, 3, 2, true);
    EXPECT_EQ(result.second.size(), x0.size());
}

TEST(MinimizeTestPublic, EdgeCaseZeroIterationsPublic) {
    std::vector<double> x0{6, 8};
    std::vector<std::pair<double, double>> bounds{{-20, 20}, {-20, 20}};
    auto result = pso::minimize(public_cost, x0, bounds, 2, 0, false);
    EXPECT_TRUE((std::is_same<decltype(result.first), double>::value || std::is_same<decltype(result.first), int>::value));
    EXPECT_EQ(result.second.size(), x0.size());
}

TEST(UpdatePositionTestPublic, HitsUpperBoundPublic) {
    std::vector<double> x0{0.7, 0.4};
    pso::Particle p(x0);
    std::vector<std::pair<double, double>> bounds{{0, 1}, {0, 1}};
    p.velocity_i = {0.0, 0.8};
    p.update_position(bounds);
    EXPECT_DOUBLE_EQ(p.position_i[1], 1.0);
    EXPECT_DOUBLE_EQ(p.position_i[0], x0[0] + p.velocity_i[0]);
}

TEST(UpdatePositionTestPublic, HitsLowerBoundPublic) {
    std::vector<double> x0{-0.8, 0.2};
    pso::Particle p(x0);
    std::vector<std::pair<double, double>> bounds{{-1, 0}, {-1, 0}};
    p.velocity_i = {-0.5, 0.0};
    p.update_position(bounds);
    EXPECT_DOUBLE_EQ(p.position_i[0], -1.0);
    EXPECT_DOUBLE_EQ(p.position_i[1], x0[1] + p.velocity_i[1]);
}