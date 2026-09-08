#include <gtest/gtest.h>
#include "underscore.h"
#include <vector>

using namespace underscore;

TEST(TestCollections, Map) {
    std::vector<int> v{1,2,3};
    std::vector<int> expected{2,4,6};
    auto r = map_(v, [](int x){return x*2;});
    EXPECT_EQ(r, expected);
}