#include "gtest/gtest.h"
#include "sample/simple.h"
#include <variant>
#include <stdexcept>

using sample::add_one;

TEST(PublicSimpleTests, AddOneLargePositive) {
    EXPECT_EQ(add_one(100), 101);
}

TEST(PublicSimpleTests, AddOneNegativeOne) {
    EXPECT_EQ(add_one(-1), 0);
}

TEST(PublicSimpleTests, AddOneLargeNegative) {
    EXPECT_EQ(add_one(-99), -98);
}

TEST(PublicSimpleTests, AddOneFloatNegative) {
    EXPECT_DOUBLE_EQ(add_one(-2.25), -1.25);
}

TEST(PublicSimpleTests, AddOneNoneRaises) {
    // Simulate: add_one with "None" (no value): should throw in C++
    EXPECT_THROW(
        {
            add_one(std::variant<int, double>{}); // empty variant
        }, std::invalid_argument);
}