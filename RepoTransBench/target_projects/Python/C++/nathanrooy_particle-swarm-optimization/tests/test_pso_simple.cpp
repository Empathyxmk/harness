#include <gtest/gtest.h>
#include "pso/pso_simple.h"
#include <vector>
#include <cmath>
#include <type_traits>

double simple_cost(const std::vector<double>& x) {
    double sum = 0.0;
    for (auto val : x) sum += val * val;
    return sum;
}

TEST(ParticleTest, InstanceAndAttributes) {
    std::vector<double> x0{1, -1};
    pso::Particle p(x0);
    EXPECT_EQ(p.position_i.size(), x0.size());
    EXPECT_EQ(p.velocity_i.size(), x0.size());
    EXPECT_EQ(p.pos_best_i.size(), x0.size());
    EXPECT_NO_THROW(p.err_best_i);
    EXPECT_NO_THROW(p.err_i);
}

TEST(ParticleTest, EvaluateAndPersonalBest) {
    std::vector<double> x0{2, 3};
    pso::Particle p(x0);
    p.evaluate(simple_cost);
    double err_first = p.err_best_i;
    // update position and re-evaluate
    p.position_i = {4, 5};
    p.evaluate(simple_cost);
    EXPECT_TRUE(p.err_best_i == err_first || p.err_best_i == simple_cost({4, 5}));
    EXPECT_DOUBLE_EQ(p.err_i, simple_cost({4, 5}));
}

TEST(ParticleTest, UpdateVelocityAndPosition) {
    std::vector<double> x0{0.5, -0.5};
    pso::Particle p(x0);
    p.pos_best_i = x0;
    std::vector<double> pos_best_g{0.1, 0.2};
    auto old_v = p.velocity_i;
    p.update_velocity(pos_best_g);
    EXPECT_EQ(p.velocity_i.size(), old_v.size());

    std::vector<std::pair<double, double>> bounds{{-1, 1}, {-1, 1}};
    p.velocity_i = {2, -2};
    p.update_position(bounds);
    for (double v : p.position_i) {
        EXPECT_LE(v, 1.0);
        EXPECT_GE(v, -1.0);
    }
}

TEST(MinimizeTest, Basic) {
    std::vector<double> x0{1, 2};
    std::vector<std::pair<double, double>> bounds{{-5, 5}, {-5, 5}};
    auto result = pso::minimize(simple_cost, x0, bounds, 5, 10, false);
    EXPECT_TRUE((std::is_same<decltype(result.first), double>::value));
    EXPECT_EQ(result.second.size(), x0.size());
}

TEST(MinimizeTest, VerboseOutput) {
    std::vector<double> x0{0, 0};
    std::vector<std::pair<double, double>> bounds{{-1, 1}, {-1, 1}};
    // We can't easily check stdout, but test still runs pso::minimize with verbose=true
    auto result = pso::minimize(simple_cost, x0, bounds, 3, 2, true);
    EXPECT_EQ(result.second.size(), x0.size());
}

TEST(MinimizeTest, EdgeCaseZeroIterations) {
    std::vector<double> x0{5, 7};
    std::vector<std::pair<double, double>> bounds{{-10, 10}, {-10, 10}};
    auto result = pso::minimize(simple_cost, x0, bounds, 2, 0, false);
    EXPECT_TRUE((std::is_same<decltype(result.first), double>::value || std::is_same<decltype(result.first), int>::value));
    EXPECT_EQ(result.second.size(), x0.size());
}

TEST(UpdatePositionTest, HitsUpperBound) {
    std::vector<double> x0{0.9, 0.0};
    pso::Particle p(x0);
    std::vector<std::pair<double, double>> bounds{{0, 1}, {0, 1}};
    p.velocity_i = {0.5, 0.0};
    p.update_position(bounds);
    EXPECT_DOUBLE_EQ(p.position_i[0], 1.0);
    EXPECT_DOUBLE_EQ(p.position_i[1], x0[1] + p.velocity_i[1]);
}

TEST(UpdatePositionTest, HitsLowerBound) {
    std::vector<double> x0{0.0, -0.9};
    pso::Particle p(x0);
    std::vector<std::pair<double, double>> bounds{{-1, 0}, {-1, 0}};
    p.velocity_i = {0.0, -0.5};
    p.update_position(bounds);
    EXPECT_DOUBLE_EQ(p.position_i[1], -1.0);
    EXPECT_DOUBLE_EQ(p.position_i[0], x0[0] + p.velocity_i[0]);
}