#include <gtest/gtest.h>
#include "haishoku/alg.h"

TEST(TestPublicHaishokuEdgeCases, test_rgb2hls_boundary) {
    EXPECT_EQ(rgb2hls({0,0,0}), std::make_tuple(0,0,0));
    EXPECT_EQ(rgb2hls({255,255,255}), std::make_tuple(0,255,0));
}