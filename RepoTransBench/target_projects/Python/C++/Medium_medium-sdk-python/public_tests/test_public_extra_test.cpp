#include <gtest/gtest.h>
#include "medium.h"

TEST(ClientInitPublicTest, TokenIsSet) {
    Client c("public_token_abc");
    EXPECT_EQ(c.token, "public_token_abc");
}