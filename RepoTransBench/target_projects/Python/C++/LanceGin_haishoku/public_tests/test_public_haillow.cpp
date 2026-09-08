#include <gtest/gtest.h>
#include "haishoku/haillow.h"

TEST(TestPublicHaillow, tuple_to_hex_public) {
    EXPECT_EQ(haillow::tuple_to_hex({12,210,111}), "#0cd26f");
}

TEST(TestPublicHaillow, hex_to_tuple_public) {
    EXPECT_EQ(haillow::hex_to_tuple("#123456"), std::make_tuple(18,52,86));
}