#include <gtest/gtest.h>
#include "shortuuid/shortuuid.h"

TEST(PublicShortUUIDInitImports, ImportMainPublic) {
    // Should successfully import the main module symbols
    EXPECT_NO_THROW({
        ShortUUID sq;
        auto code = encode("00000000-0000-0000-0000-000000000000");
        auto d = decode(code);
    });
    EXPECT_TRUE(shortuuid_hasattr("ShortUUID"));
}