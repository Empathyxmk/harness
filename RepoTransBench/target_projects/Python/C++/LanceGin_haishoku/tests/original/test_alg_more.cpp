#include <gtest/gtest.h>
#include <vector>
#include <tuple>
#include "haishoku/alg.h"

TEST(TestAlgMore, sort_by_rgb_basic) {
    std::vector<std::pair<int, std::tuple<int, int, int>>> colors = {
        {10, {52,150,70}},
        {4, {200,100,30}},
        {7, {100,120,140}}
    };
    auto result = sort_by_rgb(colors);
    std::vector<std::pair<int, std::tuple<int, int, int>>> expected = {
        {10, {52,150,70}},
        {7, {100,120,140}},
        {4, {200,100,30}}
    };
    EXPECT_EQ(result, expected);
}

TEST(TestAlgMore, rgb_maximum_basic) {
    std::vector<std::pair<int, std::tuple<int,int,int>>> colors = {
        {2, {10,20,30}},
        {5, {40,50,60}},
        {3, {25,35,45}}
    };
    auto result = rgb_maximum(colors);
    EXPECT_EQ(result["r_max"], 40);
    EXPECT_EQ(result["r_min"], 10);
    EXPECT_EQ(result["g_max"], 50);
    EXPECT_EQ(result["g_min"], 20);
    EXPECT_EQ(result["b_max"], 60);
    EXPECT_EQ(result["b_min"], 30);
    EXPECT_NEAR(result["r_dvalue"], 10.0, 1e-6);
    EXPECT_NEAR(result["g_dvalue"], 10.0, 1e-6);
    EXPECT_NEAR(result["b_dvalue"], 10.0, 1e-6);
}

TEST(TestAlgMore, group_by_accuracy_edge) {
    std::vector<std::pair<int, std::tuple<int,int,int>>> colors = {
        {2, {10,20,30}},
        {1, {11,21,31}},
    };
    auto grouped = group_by_accuracy(colors, 1);
    int found = 0;
    for (auto &rgbl : grouped)
        for (auto &rgl : rgbl)
            for (auto &cell : rgl)
                found += cell.size();
    EXPECT_EQ(found, 2);
}

TEST(TestAlgMore, group_by_accuracy_large_range) {
    std::vector<std::pair<int, std::tuple<int,int,int>>> colors = {
        {1, {0,0,0}},
        {1, {127,127,127}},
        {1, {255,255,255}},
    };
    auto grouped = group_by_accuracy(colors);
    int out = 0;
    for (int i=0;i<3;++i)
        for (int j=0;j<3;++j)
            for (int k=0;k<3;++k)
                out += grouped[i][j][k].size();
    EXPECT_EQ(out, 3);
}

TEST(TestAlgMore, get_weighted_mean_weighted) {
    std::vector<std::pair<int,std::tuple<int,int,int>>> group = {
        {10, {100,150,200}},
        {10, {110,130,170}}
    };
    auto weighted = get_weighted_mean(group);
    EXPECT_EQ(weighted.first, 20);
    EXPECT_EQ(std::get<0>(weighted.second), 105);
    EXPECT_EQ(std::get<1>(weighted.second), 140);
    EXPECT_EQ(std::get<2>(weighted.second), 185);
}

TEST(TestAlgMore, get_weighted_mean_single) {
    std::vector<std::pair<int,std::tuple<int,int,int>>> group = { {1, {1,2,3}} };
    auto weighted = get_weighted_mean(group);
    EXPECT_EQ(weighted, std::make_pair(1, std::make_tuple(1,2,3)));
}

TEST(TestAlgMore, group_by_accuracy_all_same_color) {
    std::vector<std::pair<int, std::tuple<int,int,int>>> colors = {
        {2, {10,20,30}},
        {2, {10,20,30}}
    };
    auto grouped = group_by_accuracy(colors);
    int found = 0;
    for (int i=0;i<3;++i)
        for (int j=0;j<3;++j)
            for (int k=0;k<3;++k)
                found += grouped[i][j][k].size();
    EXPECT_EQ(found, 2);
}