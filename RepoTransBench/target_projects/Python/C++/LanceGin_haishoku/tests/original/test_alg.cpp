#include <gtest/gtest.h>
#include <vector>
#include <tuple>
#include <algorithm>
#include "haishoku/alg.h"

// Mimic the Python tuple: (count, (R,G,B))
using ColorTuple = std::pair<int, std::tuple<int, int, int>>;

class TestAlg : public ::testing::Test {
protected:
    std::vector<std::pair<int, std::tuple<int, int, int>>> colors_tuple;
    std::vector<std::pair<int, std::tuple<int, int, int>>> sorted_tuple;
    void SetUp() override {
        colors_tuple = {
            {10, {100, 150, 200}},
            {5, {120, 130, 140}},
            {8, {110, 170, 130}},
            {15, {90, 80, 210}},
            {3, {180, 50, 60}},
            {2, {240, 10, 20}},
        };
        sorted_tuple = sort_by_rgb(colors_tuple);
    }
};

TEST_F(TestAlg, sort_by_rgb) {
    auto expected = colors_tuple;
    std::sort(expected.begin(), expected.end(),
              [](const ColorTuple& a, const ColorTuple& b){ return a.second < b.second; });
    auto result = sort_by_rgb(colors_tuple);
    EXPECT_EQ(expected, result);
}

TEST_F(TestAlg, rgb_maximum) {
    auto result = rgb_maximum(colors_tuple);
    EXPECT_EQ(result["r_max"], 240);
    EXPECT_EQ(result["r_min"], 90);
    EXPECT_EQ(result["g_max"], 170);
    EXPECT_EQ(result["g_min"], 10);
    EXPECT_EQ(result["b_max"], 210);
    EXPECT_EQ(result["b_min"], 20);
    EXPECT_TRUE(result.size() >= 6);
}

TEST_F(TestAlg, group_by_accuracy) {
    auto rgb = group_by_accuracy(sorted_tuple);
    EXPECT_EQ(rgb.size(), 3);
    EXPECT_EQ(rgb[0].size(), 3);
    EXPECT_EQ(rgb[0][0].size(), 3);
}

TEST_F(TestAlg, get_weighted_mean) {
    std::vector<ColorTuple> group = { {10, {100,150,200}}, {5, {120,130,140}} };
    auto w_mean = get_weighted_mean(group);
    EXPECT_EQ(w_mean.first + w_mean.second[0]+w_mean.second[1]+w_mean.second[2],
              10+5+((100*10+120*5)/15)+((150*10+130*5)/15)+((200*10+140*5)/15));
    EXPECT_EQ(std::get<0>(w_mean.second), w_mean.second[0]);
    EXPECT_EQ(std::get<1>(w_mean.second), w_mean.second[1]);
    EXPECT_EQ(std::get<2>(w_mean.second), w_mean.second[2]);
}

TEST_F(TestAlg, get_weighted_mean_single) {
    std::vector<ColorTuple> group = { {7, {50,60,70}} };
    auto w_mean = get_weighted_mean(group);
    EXPECT_EQ(w_mean, ColorTuple{7, {50,60,70}});
}

TEST_F(TestAlg, get_weighted_mean_zero) {
    std::vector<ColorTuple> group;
    EXPECT_THROW(get_weighted_mean(group), std::runtime_error);
}