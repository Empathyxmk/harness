#include <gtest/gtest.h>
#include "haishoku/haishoku.h"

TEST(TestHaishokuEdgeCases, test_Haishoku_instance_return_type) {
    auto obj = Haishoku::loadHaishoku("demo/demo_01.png");
    EXPECT_EQ(obj, typeid(Haishoku));
}