#include <gtest/gtest.h>
#include <vector>
#include <map>
#include <string>
#include "lafan1_extract.h"

TEST(TestExtract, PadAndConcatBasic) {
    std::vector<std::vector<double>> arrs = { {0,0}, {1,1} };
    auto result = pad_and_concat(arrs);
    ASSERT_EQ(result.size(), 2);
    ASSERT_EQ(result[0][0], 0.0);
    ASSERT_EQ(result[1][0], 1.0);
}

TEST(TestExtract, PadAndConcatDifferentShapes) {
    std::vector<std::vector<double>> arrs = { {0,0}, {1,1,1} };
    auto result = pad_and_concat(arrs);
    ASSERT_EQ(result.size(), 2);
}

TEST(TestExtract, FlattenDict) {
    std::map<std::string,int> d{{"a", 1}, {"b", 2}};
    auto kv = flatten_dict(d);
    ASSERT_EQ(kv.first.size(), 2);
    ASSERT_EQ(kv.second.size(), 2);
}

TEST(TestExtract, ShapeReturnsCorrect) {
    std::vector<std::vector<double>> arr(2,std::vector<double>(3,0.0));
    auto sh = shape(arr);
    ASSERT_EQ(sh[0], 2);
    ASSERT_EQ(sh[1], 3);
}

TEST(TestExtract, ShapeEmpty) {
    std::vector<std::vector<double>> arr;
    auto sh = shape(arr);
    ASSERT_EQ(sh[0], 0);
    ASSERT_EQ(sh[1], 0);
}

TEST(TestExtract, ParseBVHHierarchyAndMotion) {
    std::vector<std::string> text = {
        "HIERARCHY", "ROOT Hips", "{", "OFFSET 0.00 0.00 0.00",
        "CHANNELS 6 Xposition Yposition Zposition Zrotation Xrotation Yrotation",
        "JOINT Knee", "{", "OFFSET 0.00 1.00 0.00", "CHANNELS 3 Zrotation Xrotation Yrotation", "}", "}", "MOTION", "Frames: 2", "Frame Time: 0.0333333", "0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0", "1.0 1.0 1.0 0.5 0.5 0.5 0.1 0.2 0.3"
    };
    auto parsed = parse_bvh(text);
    ASSERT_TRUE(parsed.find("hierarchy") != parsed.end());
    ASSERT_TRUE(parsed.find("motion") != parsed.end());
    ASSERT_TRUE(parsed.find("channels") != parsed.end());
}

TEST(TestExtract, ParseBVHMalformed) {
    std::vector<std::string> lines = {"nonsense", "not bvh"};
    EXPECT_THROW({
        parse_bvh(lines);
    }, std::invalid_argument);
}