#include <gtest/gtest.h>
#include <set>
#include <vector>
#include <algorithm>

TEST(Operations, Addition) {
    int a = 2, b = 3;
    ASSERT_EQ(a + b, 5);
}

TEST(Operations, UniqueSetElements) {
    std::set<int> s{7, 8, 7, 6};
    ASSERT_EQ(s.size(), 3);
    ASSERT_NE(s.find(6), s.end());
    ASSERT_NE(s.find(7), s.end());
    ASSERT_NE(s.find(8), s.end());
}