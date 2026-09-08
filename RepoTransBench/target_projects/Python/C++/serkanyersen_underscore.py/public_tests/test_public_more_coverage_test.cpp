#include <gtest/gtest.h>
#include "underscore.h"
#include <map>
#include <string>

using namespace underscore;

TEST(TestPublicMoreCoverage, IsEmptyPublic) {
    std::map<std::string, std::string> empty_m;
    EXPECT_TRUE(is_empty(std::map<std::string,int>())); // using int values for is_empty overload
    std::map<std::string, std::string> m1{{"a", "z"}};
    std::map<std::string,int> m2{{"a",42}};
    EXPECT_FALSE(is_empty(m2));
}