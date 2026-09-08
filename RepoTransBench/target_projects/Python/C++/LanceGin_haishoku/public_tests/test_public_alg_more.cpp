#include <gtest/gtest.h>
#include "haishoku/alg.h"

TEST(TestPublicAlgMore, sort_color_variation) {
    std::map<std::tuple<int,int,int>, int> color_hist = {
        {{20,20,20}, 1},
        {{200,200,200}, 3},
        {{100,100,100}, 2}
    };
    auto result = sort_color(color_hist);
    EXPECT_EQ(result[0].first, std::make_tuple(200,200,200));
    EXPECT_EQ(result[1].first, std::make_tuple(100,100,100));
    EXPECT_EQ(result[2].first, std::make_tuple(20,20,20));
}

TEST(TestPublicAlgMore, get_color_distinct_vivid) {
    std::vector<std::tuple<int,int,int>> base = {
        {13,23,33}, {14,23,32}, {110,150,195}, {111,150,195}, {110,151,194}
    };
    auto res = get_color(base, 2);
    EXPECT_EQ(res.size(), 2);
    bool has_tuple = false;
    for(const auto& item : res)
        if(item.size() == 3) has_tuple = true;
    EXPECT_TRUE(has_tuple);
}