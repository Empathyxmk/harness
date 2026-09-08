#include <gtest/gtest.h>
#include "showme/core.h"
#include <string>

namespace {

using namespace showme::core;

TEST(PublicCoreAdditional, StringUpperTest) {
    EXPECT_EQ(upper("testing"), "TESTING");
}

TEST(PublicCoreAdditional, ArithmeticOps) {
    EXPECT_EQ(add(101, 21), 122);
    EXPECT_EQ(subtract(45, 14), 31);
    EXPECT_EQ(multiply(13, 4), 52);
    EXPECT_DOUBLE_EQ(divide(80, 4), 20.0);
    EXPECT_DOUBLE_EQ(divide(77, 5), 15.4);
    EXPECT_EQ(add(-5, -2), -7);
}

}