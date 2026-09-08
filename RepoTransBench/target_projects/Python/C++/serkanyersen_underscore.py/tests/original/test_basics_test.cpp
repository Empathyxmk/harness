#include <gtest/gtest.h>
#include "underscore.h"

using namespace underscore;

TEST(TestBasics, Identity) {
    EXPECT_EQ(identity(42), 42);
}