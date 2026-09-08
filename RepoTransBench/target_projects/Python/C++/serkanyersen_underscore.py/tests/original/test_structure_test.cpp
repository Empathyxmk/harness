#include <gtest/gtest.h>
#include "underscore.h"
#include <vector>
#include <string>
#include <map>
#include <utility>

using namespace underscore;

TEST(TestStructure, Pairs) {
    std::map<std::string,int> d{{"a",1}, {"b",2}};
    std::vector<std::pair<std::string,int>> expected{{"a",1}, {"b",2}};
    auto result = pairs(d);
    EXPECT_EQ(result, expected);
}