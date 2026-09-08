#include <gtest/gtest.h>
#include "showme/core.h"

namespace {

TEST(PublicCputime, ReturnsFloatAndNonNegative) {
    double value = showme::core::cputime();
    EXPECT_GE(value, 0.0);
    // Not possible to assert more properties portably
}

}