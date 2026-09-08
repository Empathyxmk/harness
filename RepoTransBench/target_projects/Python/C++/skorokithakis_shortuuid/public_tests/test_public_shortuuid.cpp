#include <gtest/gtest.h>
#include "shortuuid/shortuuid.h"
#include <string>
#include <algorithm>

TEST(PublicShortUUID, EncodeDiffValue) {
    std::string uuid = "11111111-1111-1111-1111-111111111111";
    auto encoded = encode(uuid);
    EXPECT_FALSE(encoded.empty());
    auto decoded = decode(encoded);
    EXPECT_EQ(decoded, uuid);
}

TEST(PublicShortUUID, EncodeEmpty) {
    std::string empty_uuid = "00000000-0000-0000-0000-000000000000";
    auto encoded = encode(empty_uuid);
    EXPECT_FALSE(encoded.empty());
    EXPECT_EQ(decode(encoded), empty_uuid);
}

TEST(PublicShortUUID, UUIDLength12) {
    ShortUUID sq;
    auto result = sq.uuid("", 12);
    EXPECT_EQ(result.size(), 12u);
}

TEST(PublicShortUUID, RandomCharset) {
    ShortUUID sq("XYabc890");
    auto r = sq.random(5);
    EXPECT_EQ(r.size(), 5u);
    EXPECT_TRUE(std::all_of(r.begin(), r.end(), [](char c){
        return std::string("XYabc890").find(c) != std::string::npos;
    }));
}

TEST(PublicShortUUID, EncodeDecodeCustomAlphabet) {
    ShortUUID sq("abc4321p");
    std::string uuid = "deadcafe-1234-4321-aaaa-1111abcdef00";
    auto s = sq.encode(uuid);
    EXPECT_EQ(sq.decode(s), uuid);
}

TEST(PublicShortUUID, UUIDAndRandomAreDistinct) {
    ShortUUID sq;
    std::string val1 = sq.uuid();
    std::string val2 = sq.random(val1.size());
    EXPECT_NE(val1, val2);
}