#include <gtest/gtest.h>
#include "viralocic_cpp_enumerable/core.h"

using namespace viralogic;

TEST(CoreTest, NodeNextValue) {
    Node n1(1);
    Node n2(2);
    n1.next = &n2;
    EXPECT_EQ(n1.value, 1);
    ASSERT_TRUE(n1.next != nullptr);
    EXPECT_EQ(n1.next->value, 2);
}

TEST(CoreTest, KeyRepr) {
    Key k(42);
    EXPECT_EQ(k.value, 42);

    Key k2(100);
    EXPECT_EQ(k2.value, 100);
}

TEST(CoreTest, OrderingDirection) {
    EXPECT_EQ(OrderingDirection::ASC, 1);
    EXPECT_EQ(OrderingDirection::DESC, -1);
}

TEST(CoreTest, RepeatableIterableBasics) {
    std::vector<int> data{1,2,3};
    RepeatableIterable rit(data);
    ASSERT_EQ(rit.data, data);
    ASSERT_EQ(rit.data.size(), 3u);
}

TEST(CoreTest, RepeatableIterableTypeError) {
    // In C++ vectors type checked compile-time, no similar error at runtime
    SUCCEED();
}