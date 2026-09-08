#include <gtest/gtest.h>
#include "helpers.h"

TEST(PublicCoreHelpers, test_shout_public) {
    EXPECT_EQ(shout("public"), "PUBLIC!");
}

TEST(PublicCoreHelpers, test_invert_bool_public_true) {
    EXPECT_FALSE(invert_bool(true));
}

TEST(PublicCoreHelpers, test_invert_bool_public_false) {
    EXPECT_TRUE(invert_bool(false));
}

TEST(PublicCoreHelpers, test_shout_public_numbers) {
    EXPECT_EQ(shout("123"), "123!");
}