#include <gtest/gtest.h>
#include "underscore.h"
#include <vector>

using namespace underscore;

TEST(TestPublicArrays, ChunkPublic) {
    std::vector<int> input{10,20,30,40,50};
    std::vector<std::vector<int>> expected{{10,20,30},{40,50}};
    auto result = chunk(input, 3);
    EXPECT_EQ(result, expected);
}

TEST(TestPublicArrays, CompactPublic) {
    // Only non-zero ints are kept
    // ['hello', 9, 5] as ints: map string/False/None types to 0s for this dummy function
    std::vector<int> input{0, 1, 0, 0, 9, 0, 5}; // mapping None, 'hello', '', 0, 9, False, 5
    std::vector<int> expected{1,9,5};
    auto result = compact(input);
    EXPECT_EQ(result, expected);
}