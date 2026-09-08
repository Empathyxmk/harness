#include <gtest/gtest.h>
#include "underscore.h"
#include <vector>

using namespace underscore;

TEST(TestMoreCoverage, IsEmpty) {
    std::vector<int> empty_v;
    EXPECT_TRUE(is_empty(empty_v));
    std::vector<int> nonempty{1};
    EXPECT_FALSE(is_empty(nonempty));
}