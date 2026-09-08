#include <gtest/gtest.h>
#include "honcho/colour.h"

TEST(TestColour, Colours) {
    EXPECT_EQ(honcho::colour::red, "31");
    EXPECT_EQ(honcho::colour::intense_red, "31;1");
    EXPECT_EQ(honcho::colour::cyan, "36");
    EXPECT_EQ(honcho::colour::intense_cyan, "36;1");
}

TEST(TestColour, GetColours) {
    auto gen = honcho::colour::get_colours();
    std::vector<std::string> expect = {
        honcho::colour::cyan,
        honcho::colour::yellow,
        honcho::colour::green,
        honcho::colour::magenta,
        honcho::colour::red,
        honcho::colour::blue
    };
    std::vector<std::string> actual;
    for (int i = 0; i < 6; ++i)
        actual.push_back(gen());
    EXPECT_EQ(expect, actual);
}