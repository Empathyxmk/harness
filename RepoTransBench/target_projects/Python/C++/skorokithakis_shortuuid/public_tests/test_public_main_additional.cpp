#include <gtest/gtest.h>
#include "shortuuid/shortuuid.h"
#include <string>
#include <algorithm>

TEST(PublicMainAdditional, EncodeDecodeInt) {
    std::string uuid = "12345678-1234-5678-1234-567812345678";
    auto encoded = encode(uuid);
    auto decoded = decode(encoded);
    EXPECT_EQ(decoded, uuid);
    EXPECT_FALSE(encoded.empty());
}

TEST(PublicMainAdditional, UuidLengthChange) {
    auto result = uuid(6);
    EXPECT_EQ(result.size(), 6u);
}

TEST(PublicMainAdditional, RandomAlphabet) {
    std::string alphabet = "xyz123uvw";
    set_alphabet(alphabet);
    std::string rand_str = random(8);
    EXPECT_EQ(rand_str.size(), 8u);
    EXPECT_TRUE(std::all_of(rand_str.begin(), rand_str.end(), [&](char c){
        return alphabet.find(c) != std::string::npos;
    }));
    EXPECT_EQ(get_alphabet(), alphabet);
}

TEST(PublicMainAdditional, ShortUUIDInstanceRandom) {
    std::string alphabet = "gfedcba098";
    ShortUUID sq(alphabet);
    auto val = sq.random(7);
    EXPECT_EQ(val.size(), 7u);
    EXPECT_TRUE(std::all_of(val.begin(), val.end(), [&](char c){
        return alphabet.find(c) != std::string::npos;
    }));
}

TEST(PublicMainAdditional, ShortUUIDInstanceUuidLength) {
    ShortUUID sq("HIJK4567LMN");
    auto val = sq.uuid("", 10); // name="", length=10
    EXPECT_EQ(val.size(), 10u);
}

TEST(PublicMainAdditional, ShortUUIDEncodeDecodeLargeInt) {
    ShortUUID sq;
    uint64_t num = 312319019ull;
    std::string uuid = int_to_uuid(num); // you must implement int->uuid string helper
    auto encoded = sq.encode(uuid);
    auto decoded = sq.decode(encoded);
    EXPECT_EQ(decoded, uuid);
    EXPECT_FALSE(encoded.empty());
}