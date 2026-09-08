#include <gtest/gtest.h>
#include "underscore.h"
#include <set>
#include <map>
#include <string>

using namespace underscore;

TEST(TestPublicObjects, KeysPublic) {
    std::map<std::string,int> d{{"x",42},{"y",100}};
    std::vector<std::string> result = keys(d);
    std::set<std::string> result_set(result.begin(), result.end());
    std::set<std::string> expected{"x","y"};
    EXPECT_EQ(result_set, expected);
}