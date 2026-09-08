#include <gtest/gtest.h>
#include <set>
#include <vector>
#include <algorithm>
#include <numeric>
#include <tuple>

TEST(PublicOperationsTest, UniqueSetElements) {
    std::set<int> s{7,8,7,6};
    EXPECT_EQ(s.size(), 3);
    EXPECT_TRUE(s.count(6) && s.count(7) && s.count(8));
}

TEST(PublicOperationsTest, SumDictKeys) {
    std::vector<int> vals{14, 12};
    EXPECT_EQ(std::accumulate(vals.begin(), vals.end(), 0), 26);
}

TEST(PublicOperationsTest, TupleConcat) {
    auto t1 = std::make_tuple(7,8);
    auto t2 = std::make_tuple(9,10);
    auto t = std::tuple_cat(t1, t2);
    EXPECT_EQ(std::get<0>(t), 7);
    EXPECT_EQ(std::get<1>(t), 8);
    EXPECT_EQ(std::get<2>(t), 9);
    EXPECT_EQ(std::get<3>(t), 10);
}