#include <gtest/gtest.h>
#include <stdexcept>
#include <map>
#include <string>
#include <vector>
#include "drawille.h"

TEST(DrawilleExtra, GetTerminalSizeEnv) {
    // Simulate: no ioctl, fallback to env
    set_env_size(100, 30);
    int width, height;
    std::tie(width, height) = getTerminalSize();
    EXPECT_EQ(width, 100);
    EXPECT_EQ(height, 30);
}

TEST(DrawilleExtra, NormalizeTypes) {
    EXPECT_EQ(normalize(5), 5);
    EXPECT_EQ(normalize(4.7), 5);
    EXPECT_THROW(normalize(std::string("a")), std::invalid_argument);
    std::vector<int> testvec = {1,2};
    EXPECT_THROW(normalize(testvec), std::invalid_argument);
}

TEST(DrawilleExtra, IntDefaultDict) {
    intdefaultdict d;
    EXPECT_TRUE(d.find('x') == d.end());
    EXPECT_EQ(d['x'], 0); // operator[] will create and set zero
}

TEST(DrawilleExtra, GetPos) {
    auto p = get_pos(4, 8);
    EXPECT_EQ(p.first, 2);
    EXPECT_EQ(p.second, 2);
    auto q = get_pos(1.4, 3.6);
    EXPECT_EQ(q.first, 0);
    EXPECT_EQ(q.second, 1);
}

TEST(DrawilleExtra, CanvasUnsetUnknownType) {
    Canvas c;
    c.set(0, 0);
    c.chars[0][0] = -1; // Simulate a non-integer (by idea), works for C++
    c.unset(0, 0); // Should not throw
    EXPECT_TRUE(c.chars[0].empty() || c.chars.find(0) == c.chars.end());
}

TEST(DrawilleExtra, CanvasSetInvalidType) {
    Canvas c;
    c.chars[0][0] = -2; // In C++, just keep as int
    c.set(0, 0); // Should not throw or affect
    EXPECT_EQ(c.chars[0][0], 1); // set will always set to 1
}

TEST(DrawilleExtra, CanvasToggleCrossType) {
    Canvas c;
    c.chars[0][0] = 88; // In C++ just set as int
    c.toggle(0,0); // Should not throw
    EXPECT_TRUE(c.chars[0].empty() || c.chars.find(0) == c.chars.end());
}

TEST(DrawilleExtra, CanvasLineEndingProperty) {
    Canvas c("END");
    EXPECT_EQ(c.line_ending, "END");
}