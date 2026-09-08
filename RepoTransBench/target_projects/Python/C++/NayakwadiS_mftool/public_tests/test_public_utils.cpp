#include <gtest/gtest.h>
#include <map>
#include <typeinfo>

TEST(TestUtilsBarebonePublic, test_basic_math_public) {
    EXPECT_EQ(2 * 3, 6);
    std::map<int, int> m;
    EXPECT_STREQ(typeid(m).name(), typeid(std::map<int, int>).name());
}