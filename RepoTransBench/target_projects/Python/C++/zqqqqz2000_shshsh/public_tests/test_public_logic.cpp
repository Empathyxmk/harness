#include <gtest/gtest.h>
#include <algorithm>

TEST(TestPublicLogic, Equality) {
    ASSERT_EQ(1 + 1, 2);
}

TEST(TestPublicLogic, EdgeMin) {
    int arr[] = {3, 2, 1};
    ASSERT_EQ(*std::min_element(arr, arr + 3), 1);
}