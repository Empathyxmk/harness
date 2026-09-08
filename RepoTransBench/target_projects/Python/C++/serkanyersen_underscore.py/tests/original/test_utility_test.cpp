#include <gtest/gtest.h>
#include "underscore.h"

using namespace underscore;

TEST(TestUtility, Random) {
    int num = random(1, 10);
    EXPECT_GE(num, 1);
    EXPECT_LE(num, 10);
}