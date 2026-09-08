#include <gtest/gtest.h>
#include "underscore.h"
#include <vector>
#include <string>
#include <map>
#include <utility>

using namespace underscore;

TEST(TestPublicStructure, PairsPublic) {
    std::map<std::string,int> d{{"foo",7}, {"bar",8}};
    std::vector<std::pair<std::string,int>> expected{{"foo",7}, {"bar",8}};
    auto result = pairs(d);
    EXPECT_EQ(result, expected);
}