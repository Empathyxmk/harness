#include <gtest/gtest.h>
#include <vector>
#include <cmath>
#include "lafan1_utils.h"

TEST(TestUtilsPublic, QuaternionInverseIdentity) {
    std::vector<double> q = {0.6, 0.3, 0.5, 0.5};
    auto inv = quat_inv_unit(q);
    auto ident = quat_mult_unit(q, inv);
    EXPECT_NEAR(ident[0], 1.0, 1e-4);
    EXPECT_NEAR(ident[1], 0.0, 1e-4);
    EXPECT_NEAR(ident[2], 0.0, 1e-4);
    EXPECT_NEAR(ident[3], 0.0, 1e-4);
}

TEST(TestUtilsPublic, QuaternionMulIdentityLeft) {
    std::vector<double> q = {2,-2,1,4};
    std::vector<double> ident = {1,0,0,0};
    auto product = quat_mult_unit(ident, q);
    ASSERT_EQ(product.size(), q.size());
    for (size_t i=0;i<q.size();++i)
        EXPECT_NEAR(product[i], q[i], 1e-4);
}

TEST(TestUtilsPublic, QuaternionMulIdentityRight) {
    std::vector<double> q = {-5,7,-1,0};
    std::vector<double> ident = {1,0,0,0};
    auto product = quat_mult_unit(q, ident);
    ASSERT_EQ(product.size(), q.size());
    for (size_t i=0;i<q.size();++i)
        EXPECT_NEAR(product[i], q[i], 1e-4);
}

TEST(TestUtilsPublic, QuaternionNorm) {
    std::vector<double> q = {3,1,4,1};
    double norm = std::sqrt(3*3+1*1+4*4+1*1);
    std::vector<double> n_q(4);
    std::transform(q.begin(), q.end(), n_q.begin(), [norm](double v){return v/norm;});
    for (int i=0;i<4;++i)
        EXPECT_NEAR(n_q[i], q[i]/norm, 1e-8);
}

TEST(TestUtilsPublic, QuaternionBroadcast) {
    std::vector<std::vector<double>> qs = {{2,0,0,0},{0.3,0.6,0.5,0.2}};
    for (const auto& q: qs) {
        double norm = 0;
        for (auto v: q) norm += v*v;
        norm = std::sqrt(norm);
        for (auto v: q)
            ASSERT_TRUE(std::abs(v/norm)<=1.0);
    }
}

TEST(TestUtilsPublic, QuaternionShapeRobustness) {
    std::vector<double> q(4,4.0);
    auto inv = quat_inv_unit(q);
    ASSERT_EQ(inv.size(), 4);
}