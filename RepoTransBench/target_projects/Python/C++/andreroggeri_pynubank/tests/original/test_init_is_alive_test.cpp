#include <gtest/gtest.h>
#include "pynubank/init.h"

TEST(InitIsAliveTest, ReturnsTrueIfAlive) {
    EXPECT_TRUE(is_alive());
}