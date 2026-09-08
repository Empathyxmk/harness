#include <gtest/gtest.h>
#include "ope.h"
#include "errors.h"

class TestValueRange : public ::testing::Test {};

TEST_F(TestValueRange, RangeSimple) {
    int start = 2;
    int end = 1000;
    ValueRange r(start, end);
    EXPECT_EQ(r.size(), 999);
    for (int i = start; i <= end; ++i) {
        EXPECT_TRUE(r.contains(i));
    }
    EXPECT_FALSE(r.contains(start - 1));
    EXPECT_FALSE(r.contains(end + 1));
    EXPECT_EQ(r.range_bit_size(), 10);
}

TEST_F(TestValueRange, RangeRepr) {
    ValueRange a(1, 10);
    // We'll assume repr() gives a string that can be parsed similarly.
    ValueRange b = ValueRange::fromString(a.repr());
    EXPECT_EQ(b, a);
}

TEST_F(TestValueRange, InvalidRangeEnds) {
    // Try invalid start/end values
    EXPECT_THROW({
        ValueRange("123", 0);
    }, InvalidRangeLimitsError);

    EXPECT_THROW({
        ValueRange(0, "123");
    }, InvalidRangeLimitsError);

    EXPECT_THROW({
        ValueRange("123", "abc");
    }, InvalidRangeLimitsError);
}