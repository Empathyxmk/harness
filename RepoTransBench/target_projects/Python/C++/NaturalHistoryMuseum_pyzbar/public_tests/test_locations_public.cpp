#include <gtest/gtest.h>
#include "pyzbar/locations.h"
#include <vector>

TEST(LocationsPublic, PolygonFromBbox) {
    auto bbox = std::make_tuple(3, 4, 16, 22);
    auto polygon = polygon_from_bbox(bbox);
    std::vector<Rect> expected = {Rect(3, 4), Rect(16, 4), Rect(16,22), Rect(3,22)};
    EXPECT_EQ(polygon, expected);
}

TEST(LocationsPublic, PolygonFromBboxZeroWidthHeight) {
    auto bbox = std::make_tuple(10, 10, 10, 25);
    auto polygon = polygon_from_bbox(bbox);
    std::vector<Rect> expected = {Rect(10,10), Rect(10,10), Rect(10,25), Rect(10,25)};
    EXPECT_EQ(polygon, expected);
}