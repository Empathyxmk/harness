#include <gtest/gtest.h>
#include "underscore.h"
#include <vector>

using namespace underscore;

TEST(TestFunctions, Once) {
    std::vector<int> called;
    auto func = [&called](){called.push_back(1); return 3;};
    auto once_func = once(func);
    EXPECT_EQ(once_func(), 3);
    once_func();
    std::vector<int> expected{1};
    EXPECT_EQ(called, expected);
}