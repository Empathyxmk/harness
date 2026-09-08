#include <gtest/gtest.h>
#include <vector>
#include <typeinfo>

TEST(TestUtilsBarebone, test_basic_math) {
    EXPECT_EQ(1 + 1, 2);
    std::vector<int> v;
    // Make sure typeid doesn't throw and type is std::vector<int, ...>
    EXPECT_STREQ(typeid(v).name(), typeid(std::vector<int>).name());
}