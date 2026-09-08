#include <gtest/gtest.h>
#include "pyzbar/locations.h"
#include <vector>
#include <tuple>

class LocationsTest : public ::testing::Test {};

TEST_F(LocationsTest, BoundingBox) {
    // Passing empty should throw; we check for exception
    EXPECT_THROW(bounding_box({}), std::invalid_argument);

    // Single point case
    std::vector<std::pair<int,int>> single = { {0,0} };
    EXPECT_EQ(Rect(0,0,0,0), bounding_box(single));

    // Rectangle box
    std::vector<std::pair<int,int>> pts = { {37,551},{37,625}, {361,626},{361,550}};
    EXPECT_EQ(Rect(37,550,324,76), bounding_box(pts));
}

TEST_F(LocationsTest, ConvexHullEmpty) {
    std::vector<std::pair<int,int>> pts;
    EXPECT_EQ(convex_hull(pts), std::vector<std::pair<int,int>>());
}

TEST_F(LocationsTest, ConvexSquare) {
    std::vector<std::pair<int,int>> pts = { {0,0},{0,1},{1,1},{1,0} };
    EXPECT_EQ(pts, convex_hull(pts));
}

TEST_F(LocationsTest, ConvexDuplicates) {
    std::vector<std::pair<int,int>> pts = { {0,0},{0,1},{1,1},{1,0} };
    std::vector<std::pair<int,int>> pts10;
    for (int i=0;i<10;++i) pts10.insert(pts10.end(), pts.begin(), pts.end());
    EXPECT_EQ(pts, convex_hull(pts10));
}

TEST_F(LocationsTest, ConvexHullOther) {
    auto res = convex_hull({{1,1},{2,2},{3,3},{1,3}});
    std::vector<std::pair<int,int>> expected = { {1,1},{1,3},{3,3} };
    EXPECT_EQ(expected, res);

    std::vector<std::pair<double,double>> pts = {
        {4.4, 14}, {6.7, 15.25}, {6.9, 12.8}, {2.1, 11.1}, {9.5, 14.9},
        {13.2, 11.9}, {10.3, 12.3}, {6.8, 9.5}, {3.3, 7.7}, {0.6, 5.1},
        {5.3, 2.4}, {8.45, 4.7}, {11.5, 9.6}, {13.8, 7.3}, {12.9, 3.1},
        {11, 1.1}
    };
    std::vector<std::pair<double,double>> exp = {
        {0.6,5.1}, {2.1,11.1}, {4.4,14}, {6.7,15.25}, {9.5,14.9},
        {13.2,11.9}, {13.8,7.3}, {12.9,3.1}, {11, 1.1}, {5.3,2.4}
    };
    EXPECT_EQ(exp, convex_hull(pts));
}