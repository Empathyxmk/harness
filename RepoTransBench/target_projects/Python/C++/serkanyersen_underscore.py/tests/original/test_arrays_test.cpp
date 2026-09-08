#include <gtest/gtest.h>
#include "underscore.h"
#include <vector>

using namespace underscore;

TEST(TestArrays, Chunk) {
    std::vector<int> input{1,2,3,4};
    std::vector<std::vector<int>> expected{{1,2},{3,4}};
    auto result = chunk(input, 2);
    EXPECT_EQ(result, expected);
}

TEST(TestArrays, Compact) {
    std::vector<int> input{0,1,0,2,0,3};
    std::vector<int> filter_expected{1,2,3};
    auto result = compact(input);
    EXPECT_EQ(result, filter_expected);
}