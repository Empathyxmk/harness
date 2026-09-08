#include <gtest/gtest.h>
#include <map>
#include <string>
#include "lib/OPACK.h"

TEST(OPACKSuite, EncodeDecodeDict) {
    std::map<std::string, int> data {{"pf", 266256}};
    std::vector<uint8_t> encoded = OPACK::encode(data);
    auto decoded = OPACK::decode(encoded);
    EXPECT_EQ(data, decoded);
}