#include <gtest/gtest.h>
#include <string>
#include <vector>

class PublicParamsTest : public ::testing::TestWithParam<std::string> {};

INSTANTIATE_TEST_SUITE_P(PublicFruits, PublicParamsTest, ::testing::Values("orange", "grape"));

TEST_P(PublicParamsTest, FruitPublic) {
    std::string fruit = GetParam();
    (void)fruit;
    EXPECT_TRUE(true); // Always true as in original python
}