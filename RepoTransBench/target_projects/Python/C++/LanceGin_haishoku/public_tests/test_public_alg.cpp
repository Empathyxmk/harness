#include <gtest/gtest.h>
#include "haishoku/alg.h"

TEST(TestPublicAlg, rgb2hls_variation) {
    auto res = rgb2hls({200, 150, 100});
    EXPECT_EQ(res, std::make_tuple(30, 150, 102));
}

TEST(TestPublicAlg, get_histogram_variation) {
    std::vector<std::tuple<int,int,int>> input = { {100,100,100}, {100,100,100}, {50,50,50} };
    auto hist = get_histogram(input);
    EXPECT_EQ(hist[std::make_tuple(100,100,100)], 2);
    EXPECT_EQ(hist[std::make_tuple(50,50,50)], 1);
}