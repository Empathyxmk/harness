#include "gtest/gtest.h"
#include "lib/helper.h"

TEST(TestPublicHelper, PublicClsNameForBool) {
    EXPECT_EQ(cls_name(true), "bool");
}

TEST(TestPublicHelper, PublicClsNameForTuple) {
    std::tuple<int> t(1);
    EXPECT_EQ(cls_name(t), "tuple");
}