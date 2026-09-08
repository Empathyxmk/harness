#include <gtest/gtest.h>
#include "util.h"

TEST(Utils, BitStringConversion) {
    std::vector<uint8_t> empty;
    EXPECT_EQ(str_to_bitstring(empty), std::vector<int>{});

    std::vector<uint8_t> v1 = {'A'};
    EXPECT_EQ(str_to_bitstring(v1), std::vector<int>({0,1,0,0,0,0,0,1}));

    std::vector<uint8_t> v2 = {'A','B'};
    EXPECT_EQ(str_to_bitstring(v2), std::vector<int>({0,1,0,0,0,0,0,1, 0,1,0,0,0,0,1,0}));
}