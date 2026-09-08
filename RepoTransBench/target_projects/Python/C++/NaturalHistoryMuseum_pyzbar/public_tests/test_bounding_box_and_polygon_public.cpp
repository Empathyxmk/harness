#include <gtest/gtest.h>
#include "pyzbar/locations.h"
#include <vector>

TEST(BoundingBoxAndPolygonPublic, BoundingBoxRect) {
    std::vector<Rect> pts = {Rect(5, 7), Rect(25, 7), Rect(25, 32), Rect(5, 32)};
    auto box = bounding_box(pts);
    EXPECT_EQ(box, std::make_tuple(5, 7, 25, 32));
    std::vector<Rect> pts_reorder = {Rect(25, 32), Rect(25, 7), Rect(5, 32), Rect(5, 7)};
    auto box2 = bounding_box(pts_reorder);
    EXPECT_EQ(box2, std::make_tuple(5, 7, 25, 32));
}

TEST(BoundingBoxAndPolygonPublic, BoundingBoxNegativeCoords) {
    std::vector<Rect> pts = {Rect(-12, -8), Rect(0, -8), Rect(0, 2), Rect(-12, 2)};
    EXPECT_EQ(bounding_box(pts), std::make_tuple(-12, -8, 0, 2));
}