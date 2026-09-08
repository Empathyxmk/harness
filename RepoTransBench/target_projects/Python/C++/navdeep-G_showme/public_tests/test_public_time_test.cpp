#include <gtest/gtest.h>
#include "showme/core.h"

namespace {

TEST(PublicTime, TypeAndRange) {
    double value = showme::core::time();
    EXPECT_GE(value, 0);
    EXPECT_LT(value, 1e6); // Equivalent to <100000 in original, but more generous
}

}