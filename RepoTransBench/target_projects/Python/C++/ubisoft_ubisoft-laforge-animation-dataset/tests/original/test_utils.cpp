#include <gtest/gtest.h>
#include <vector>
#include <cmath>
#include <algorithm>
#include "lafan1_utils.h"

TEST(TestUtils, QuatInvUnitIdentity) {
    std::vector<double> x = {1., 0., 0., 0.};
    auto inv = quat_inv_unit(x);
    auto qm = quat_mult_unit(x, inv);
    EXPECT_NEAR(qm[0], 1.0, 1e-8);
    EXPECT_NEAR(qm[1], 0.0, 1e-8);
    EXPECT_NEAR(qm[2], 0.0, 1e-8);
    EXPECT_NEAR(qm[3], 0.0, 1e-8);
}

TEST(TestUtils, QuatMultUnitBasic) {
    std::vector<double> x = {1., 0., 0., 0.};
    std::vector<double> y = {1., 0., 0., 0.};
    auto z = quat_mult_unit(x, y);
    EXPECT_NEAR(z[0], 1.0, 1e-8);
    EXPECT_NEAR(z[1], 0.0, 1e-8);
    EXPECT_NEAR(z[2], 0.0, 1e-8);
    EXPECT_NEAR(z[3], 0.0, 1e-8);
}

TEST(TestUtils, QuatMultUnitNontrivial) {
    std::vector<double> x = {0., 1., 0., 0.};
    std::vector<double> y = {0., 0., 1., 0.};
    auto z = quat_mult_unit(x, y);
    std::vector<double> want = {0.,0.,0.,1.};
    std::vector<double> zabs(z.size()), wantabs(want.size());
    std::transform(z.begin(), z.end(), zabs.begin(), [](double v) { return std::abs(v); });
    std::transform(want.begin(), want.end(), wantabs.begin(), [](double v) { return std::abs(v); });
    std::sort(zabs.begin(), zabs.end());
    std::sort(wantabs.begin(), wantabs.end());
    for (int i = 0; i < 4; ++i)
        EXPECT_NEAR(zabs[i], wantabs[i], 1e-8);
}

TEST(TestUtils, QuatMultUnitBroadcast) {
    std::vector<std::vector<double>> q1 = {{1,0,0,0},{0,1,0,0}};
    std::vector<std::vector<double>> q2 = {{1,0,0,0},{0,1,0,0}};
    auto z = quat_mult_unit(q1, q2);
    ASSERT_EQ(z.size(), 2);
    ASSERT_EQ(z[0].size(), 4);
}

TEST(TestUtils, QuatMultUnitBadShape) {
    std::vector<double> x = {1,0,0};
    std::vector<double> y = {1,0,0,0};
    EXPECT_THROW({
        quat_mult_unit(x, y);
    }, std::invalid_argument);
}

TEST(TestUtils, QuatFkWrongShape) {
    std::vector<std::vector<double>> lrot(2, std::vector<double>(4,0.));
    std::vector<std::vector<double>> lpos(3, std::vector<double>(3,0.));
    std::vector<int> parents = {-1, 0};
    std::vector<std::vector<double>> r, p;
    EXPECT_THROW({
        quat_fk(lrot, lpos, parents, r, p);
    }, std::invalid_argument);
}

TEST(TestUtils, QuatFkBadNumParents) {
    std::vector<std::vector<double>> lrot(2, std::vector<double>(4,0.));
    std::vector<std::vector<double>> lpos(2, std::vector<double>(3,0.));
    std::vector<int> parents = {-1, 1, 5};
    std::vector<std::vector<double>> r, p;
    EXPECT_THROW({
        quat_fk(lrot, lpos, parents, r, p);
    }, std::invalid_argument);
}

TEST(TestUtils, QuatFkRootLinked) {
    std::vector<std::vector<double>> lrot(2, std::vector<double>(4,0.));
    std::vector<std::vector<double>> lpos(2, std::vector<double>(3,1.));
    std::vector<int> parents = {-1, 0};
    std::vector<std::vector<double>> grot, gpos;
    quat_fk(lrot, lpos, parents, grot, gpos);
    ASSERT_EQ(grot.size(), 2);
    ASSERT_EQ(grot[0].size(), 4);
    ASSERT_EQ(gpos.size(), 2);
    ASSERT_EQ(gpos[0].size(), 3);
}