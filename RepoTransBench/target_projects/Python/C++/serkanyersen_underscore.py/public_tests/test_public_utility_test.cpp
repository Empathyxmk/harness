#include <gtest/gtest.h>
#include "underscore.h"

using namespace underscore;

TEST(TestPublicUtility, RandomPublic) {
    int num = random(20, 25);
    EXPECT_GE(num, 20);
    EXPECT_LE(num, 25);
}