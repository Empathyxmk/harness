#include <gtest/gtest.h>
#include "hgd.h"
#include "ope.h"
#include "stat.h"
#include <vector>
#include <numeric>
#include <iterator>

TEST(Stat, Uniform) {
    // Short ranges
    int value = 10;
    ValueRange unit_range(value, value);
    EXPECT_EQ(sample_uniform(unit_range, {}), value);

    ValueRange short_range(value, value+1);
    EXPECT_EQ(sample_uniform(short_range, {0}), value);
    EXPECT_EQ(sample_uniform(short_range, {1}), value + 1);
    EXPECT_EQ(sample_uniform(short_range, {0,0,1,0,0}), value);

    // Should throw
    EXPECT_THROW({
        sample_uniform(short_range, {});
    }, std::exception);

    // Medium ranges
    int start_range = 20;
    int end_range = start_range + 15;
    ValueRange range1(start_range, end_range);

    EXPECT_EQ(sample_uniform(range1, {0,0,0,0}), start_range);
    EXPECT_EQ(sample_uniform(range1, {0,0,0,1}), start_range+1);
    EXPECT_EQ(sample_uniform(range1, {1,1,1,1}), end_range);

    // With generator: We'll just simulate repeat 0
    std::vector<int> rep10(10, 0);
    EXPECT_EQ(sample_uniform(range1, rep10), start_range);

    // Negative range
    start_range = -32;
    end_range = -17;
    ValueRange negative_range(start_range, end_range);
    EXPECT_EQ(sample_uniform(negative_range, std::vector<int>(5,0)), start_range);
    EXPECT_EQ(sample_uniform(negative_range, std::vector<int>(5,1)), end_range);

    // Mixed range
    start_range = -32;
    end_range = 31;
    ValueRange mixed_range(start_range, end_range);
    EXPECT_EQ(sample_uniform(mixed_range, std::vector<int>(6,0)), start_range);
    EXPECT_EQ(sample_uniform(mixed_range, std::vector<int>(6,1)), end_range);
}

TEST(Stat, Hypergeometric) {
    struct FakeCoins {
        int val;
        FakeCoins(int x=0):val(x){}
        int next() { return val++; }
    };

    // Small values (simulate infinite coin stream by always returning 0 for simplicity)
    std::vector<int> coins(10, 0);
    EXPECT_EQ(HGD::rhyper(5, 0, 5, coins), 0);
    EXPECT_EQ(HGD::rhyper(6, 6, 0, coins), 6);

    // Large values
    EXPECT_EQ(HGD::rhyper((uint64_t)1 << 32, 0, (uint64_t)1 << 32, coins), 0);
    EXPECT_EQ(HGD::rhyper((uint64_t)1 << 64, (uint64_t)1 << 64, 0, coins), (uint64_t)1 << 64);
    EXPECT_EQ(HGD::rhyper((uint64_t)1 << 32, 2, ((uint64_t)1 << 32)-2, coins), 2);
}