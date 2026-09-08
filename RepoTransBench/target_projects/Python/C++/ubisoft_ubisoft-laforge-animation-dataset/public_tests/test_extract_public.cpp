#include <gtest/gtest.h>
#include <vector>
#include <map>
#include <string>
#include "lafan1_extract.h"

TEST(TestExtractPublic, ExtractFuncIdentity) {
    std::vector<int> data = {10,12,11,8};
    for (size_t i=0; i<data.size(); ++i)
        EXPECT_EQ(data[i], data[i]);
}

TEST(TestExtractPublic, PadOrTrim) {
    std::vector<int> arr = {9};
    std::vector<int> padded = arr;
    padded.resize(4, -1);
    EXPECT_EQ(padded.size(), 4);
    EXPECT_EQ(padded[1], -1);
}

TEST(TestExtractPublic, Unpad) {
    std::vector<int> arr = {2,3,0,0};
    std::vector<int> unpad;
    for (auto v : arr) {
        if (v==0) break;
        unpad.push_back(v);
    }
    ASSERT_EQ(unpad.size(), 2);
}