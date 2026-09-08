#include <gtest/gtest.h>
#include "haishoku/haishoku.h"

TEST(TestHaishoku, test_Haishoku_instance) {
    // In Python: returns class (not an object), so mimic that
    auto obj = Haishoku::loadHaishoku("demo/demo_01.png");
    EXPECT_EQ(obj, typeid(Haishoku));
    // Further tests can be implemented once the function is properly defined.
}