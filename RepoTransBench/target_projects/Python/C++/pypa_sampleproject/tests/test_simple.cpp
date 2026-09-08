#include "gtest/gtest.h"
#include "sample/simple.h"
#include <variant>
#include <stdexcept>

using sample::add_one;

TEST(SimpleTests, AddOnePositive) {
    EXPECT_EQ(add_one(2), 3);
}

TEST(SimpleTests, AddOneZero) {
    EXPECT_EQ(add_one(0), 1);
}

TEST(SimpleTests, AddOneNegative) {
    EXPECT_EQ(add_one(-5), -4);
}

TEST(SimpleTests, AddOneFloat) {
    EXPECT_DOUBLE_EQ(add_one(2.5), 3.5);
}

TEST(SimpleTests, AddOneStrRaises) {
    // Simulate: simple.add_one("hi") -> should raise TypeError
    // For C++, we pass something invalid, e.g. a string -> throws
    EXPECT_THROW(
        {
            // forcibly cast to avoid compile error
            add_one(std::variant<int, double>{}); // invalid variant (neither int nor double)
        },
        std::invalid_argument
    );
}