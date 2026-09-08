#include <gtest/gtest.h>
#include "underscore.h"
#include <set>
#include <map>
#include <string>

using namespace underscore;

TEST(TestObjects, Keys) {
    std::map<std::string,int> d{{"a",1}, {"b",2}};
    std::vector<std::string> result = keys(d);
    std::set<std::string> result_set(result.begin(), result.end());
    std::set<std::string> expected{"a","b"};
    EXPECT_EQ(result_set, expected);
}