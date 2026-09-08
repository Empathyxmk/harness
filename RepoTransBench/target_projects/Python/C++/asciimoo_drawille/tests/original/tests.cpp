#include <gtest/gtest.h>
#include <string>
#include <map>
#include <vector>
#include "drawille.h"

TEST(CanvasTest, Set) {
    Canvas c;
    c.set(0, 0);
    EXPECT_TRUE(c.chars.count(0) > 0 && c.chars[0].count(0) > 0);
}

TEST(CanvasTest, UnsetEmpty) {
    Canvas c;
    c.set(1, 1);
    c.unset(1, 1);
    EXPECT_EQ(c.chars.size(), 0);
}

TEST(CanvasTest, UnsetNonempty) {
    Canvas c;
    c.set(0, 0);
    c.set(0, 1);
    c.unset(0, 1);
    EXPECT_EQ(c.chars[0][0], 1);
}

TEST(CanvasTest, Clear) {
    Canvas c;
    c.set(1, 1);
    c.clear();
    EXPECT_EQ(c.chars.size(), 0);
}

TEST(CanvasTest, Toggle) {
    Canvas c;
    c.toggle(0, 0);
    EXPECT_EQ(c.chars[0][0], 1);
    c.toggle(0, 0);
    EXPECT_EQ(c.chars.size(), 0);
}

TEST(CanvasTest, SetText) {
    Canvas c;
    c.set_text(0, 0, "asdf");
    EXPECT_EQ(c.frame(), "asdf");
}

TEST(CanvasTest, Frame) {
    Canvas c;
    EXPECT_EQ(c.frame(), "");
    c.set(0, 0);
    EXPECT_EQ(c.frame(), "\u2801");
}

TEST(CanvasTest, MaxMinLimits) {
    Canvas c;
    c.set(0, 0);
    EXPECT_EQ(c.frame(2), "");
    EXPECT_EQ(c.frame(-9999, 0), "");
}

TEST(CanvasTest, Get) {
    Canvas c;
    EXPECT_FALSE(c.get(0, 0));
    c.set(0, 0);
    EXPECT_TRUE(c.get(0, 0));
    EXPECT_FALSE(c.get(0, 1));
    EXPECT_FALSE(c.get(1, 0));
    EXPECT_FALSE(c.get(1, 1));
}

TEST(LineTest, SinglePixel) {
    auto pts = line(0, 0, 0, 0);
    ASSERT_EQ(pts.size(), 1);
    EXPECT_EQ(pts[0], std::make_pair(0, 0));
}

TEST(LineTest, Row) {
    auto pts = line(0, 0, 1, 0);
    ASSERT_EQ(pts.size(), 2);
    EXPECT_EQ(pts[0], std::make_pair(0, 0));
    EXPECT_EQ(pts[1], std::make_pair(1, 0));
}

TEST(LineTest, Column) {
    auto pts = line(0, 0, 0, 1);
    ASSERT_EQ(pts.size(), 2);
    EXPECT_EQ(pts[0], std::make_pair(0, 0));
    EXPECT_EQ(pts[1], std::make_pair(0, 1));
}

TEST(LineTest, Diagonal) {
    auto pts = line(0, 0, 1, 1);
    ASSERT_EQ(pts.size(), 2);
    EXPECT_EQ(pts[0], std::make_pair(0, 0));
    EXPECT_EQ(pts[1], std::make_pair(1, 1));
}

TEST(TurtleTest, Position) {
    Turtle t;
    EXPECT_EQ(t.pos_x, 0); EXPECT_EQ(t.pos_y, 0);
    t.move(1, 1);
    EXPECT_EQ(t.pos_x, 1); EXPECT_EQ(t.pos_y, 1);
}

TEST(TurtleTest, Rotation) {
    Turtle t;
    EXPECT_EQ(t.rotation, 0);
    t.right(30);
    EXPECT_EQ(t.rotation, 30);
    t.left(30);
    EXPECT_EQ(t.rotation, 0);
}

TEST(TurtleTest, Brush) {
    Turtle t;
    EXPECT_FALSE(t.get(t.pos_x, t.pos_y));
    t.forward(1);
    EXPECT_TRUE(t.get(0, 0));
    EXPECT_TRUE(t.get(t.pos_x, t.pos_y));
    t.up();
    t.move(2, 0);
    EXPECT_FALSE(t.get(t.pos_x, t.pos_y));
    t.down();
    t.move(3, 0);
    EXPECT_TRUE(t.get(t.pos_x, t.pos_y));
}