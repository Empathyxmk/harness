#include <gtest/gtest.h>
#include "haishoku/haishoku.h"

TEST(TestPublicHaishokuClass, haishoku_main_color_distinct) {
    Haishoku hs("demo/demo_01.png");
    auto main = hs.getMainColor();
    EXPECT_GE(std::get<0>(main), 0); EXPECT_LE(std::get<0>(main), 255);
    EXPECT_GE(std::get<1>(main), 0); EXPECT_LE(std::get<1>(main), 255);
    EXPECT_GE(std::get<2>(main), 0); EXPECT_LE(std::get<2>(main), 255);
    EXPECT_NE(main, std::make_tuple(199,146,117));
}