#include <gtest/gtest.h>
#include <stdexcept>
#include <map>
#include <string>
#include <vector>
#include "drawille.h"

TEST(DrawillePublic, GetTerminalSizeEnv) {
    set_env_size(100, 33);
    int width, height;
    std::tie(width, height) = getTerminalSize();
    EXPECT_EQ(width, 100);
    EXPECT_EQ(height, 33);
}

TEST(DrawillePublic, NormalizeTypes) {
    EXPECT_EQ(normalize(15), 15);
    EXPECT_EQ(normalize(17.8), 18);
    EXPECT_THROW(normalize(std::vector<int>{}), std::invalid_argument);
    EXPECT_THROW(normalize(std::string("xyz")), std::invalid_argument);
}

TEST(DrawillePublic, IntDefaultDict) {
    intdefaultdict d;
    EXPECT_EQ(d[222], 0);
    d[222] += 55;
    EXPECT_EQ(d[222], 55);
}

TEST(DrawillePublic, GetPos) {
    auto p = get_pos(7, 9);
    EXPECT_EQ(p.first, 3);
    EXPECT_EQ(p.second, 2);
    auto q = get_pos(4.9, 15.2);
    EXPECT_EQ(q.first, 2);
    EXPECT_EQ(q.second, 3);
}

TEST(DrawillePublic, CanvasUnsetUnknownType) {
    Canvas c;
    c.set(4, 10);
    c.chars[4][10] = 999; // simulate out-of-type value
    c.unset(4, 10);
    EXPECT_TRUE(c.chars[4].empty() || c.chars.find(4) == c.chars.end());
}

TEST(DrawillePublic, CanvasSetInvalidType) {
    Canvas c;
    c.chars[6][7] = 999; // simulate
    c.set(6, 7);
    EXPECT_EQ(c.chars[6][7], 1);
}

TEST(DrawillePublic, CanvasToggleCrossType) {
    Canvas c;
    c.chars[9][12] = 0;
    c.toggle(9, 12);
    EXPECT_TRUE(c.chars[9].empty() || c.chars.find(9) == c.chars.end());
}

TEST(DrawillePublic, CanvasLineEndingProperty) {
    Canvas c("LF");
    EXPECT_EQ(c.line_ending, "LF");
}