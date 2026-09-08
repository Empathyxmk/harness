#include <gtest/gtest.h>
#include "medium.h"

TEST(ClientInitExtraTest, TokenIsSet) {
    Client c("12345");
    EXPECT_EQ(c.token, "12345");
}