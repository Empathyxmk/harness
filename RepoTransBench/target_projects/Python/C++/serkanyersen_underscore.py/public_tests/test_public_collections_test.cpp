#include <gtest/gtest.h>
#include "underscore.h"
#include <vector>

using namespace underscore;

TEST(TestPublicCollections, MapPublic) {
    std::vector<int> v{4,5,6};
    std::vector<int> expected{5,6,7};
    auto r = map_(v, [](int x){return x+1;});
    EXPECT_EQ(r, expected);
}