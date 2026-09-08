#include <gtest/gtest.h>
#include "haishoku/haishoku.h"

TEST(TestPublicHaishoku, haishoku_get_palette_public) {
    Haishoku hs("demo/demo_01.png");
    const auto& palette = hs.getPalette();
    EXPECT_EQ(palette.size(), 6);
    for(const auto& color : palette) {
        EXPECT_EQ(std::tuple_size<decltype(color)>::value, 3);
    }
}