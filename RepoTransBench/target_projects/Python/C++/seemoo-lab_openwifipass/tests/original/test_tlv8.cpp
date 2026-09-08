#include <gtest/gtest.h>
#include <vector>
#include "lib/TLV8.h"

TEST(TLV8Box, DecodeEncode) {
    std::vector<uint8_t> encoded = {0x44, 0x01, 0xFF, 0x44, 0x02, 0xFF, 0xFF};
    auto decoded = TLV8Box::decodeFromData(encoded);
    EXPECT_EQ(encoded, decoded.encode());
}