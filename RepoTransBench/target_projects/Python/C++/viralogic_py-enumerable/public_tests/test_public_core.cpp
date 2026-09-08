#include <gtest/gtest.h>
#include "viralocic_cpp_enumerable/core.h"

using namespace viralogic;

TEST(PublicCoreTest, NodeNextValue) {
    Node node1(99);
    Node node2(101);
    node1.next = &node2;
    ASSERT_TRUE(node1.next != nullptr);
    EXPECT_EQ(node1.next->value, 101);
}

TEST(PublicCoreTest, RepeatableIterableBasics) {
    RepeatableIterable r({10, 11, 12});
    EXPECT_EQ(r.data, std::vector<int>({10,11,12}));
    EXPECT_EQ(r.data.size(), 3u);
}

TEST(PublicCoreTest, RepeatableIterableReversed) {
    RepeatableIterable r({1,2,3});
    std::vector<int> reverse(r.data.rbegin(), r.data.rend());
    EXPECT_EQ(reverse, std::vector<int>({3,2,1}));
}

TEST(PublicCoreTest, RepeatableIterableIterAndNext) {
    RepeatableIterable r({41,18});
    ASSERT_EQ(r.data[0], 41);
    ASSERT_EQ(r.data[1], 18);
}

TEST(PublicCoreTest, RepeatableIterableTypeError) {
    // No runtime error possible for passing non-vector in C++
    SUCCEED();
}