#include <gtest/gtest.h>
#include <string>
#include <vector>

class ParamsTest : public ::testing::TestWithParam<std::string> {};

INSTANTIATE_TEST_SUITE_P(Fruits, ParamsTest, ::testing::Values("apple", "banana"));

TEST_P(ParamsTest, fruit) {
    std::string fruit = GetParam();
    (void)fruit; // suppress unused warning
    EXPECT_TRUE(true);
}