#include <gtest/gtest.h>
#include "pynubank/init.h"

TEST(PublicInitIsAliveTest, IsAlive) {
    EXPECT_TRUE(is_alive());
}