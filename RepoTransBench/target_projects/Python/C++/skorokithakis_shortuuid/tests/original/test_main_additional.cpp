#include <gtest/gtest.h>
#include "shortuuid/shortuuid.h"
#include <uuid/uuid.h>
#include <string>
#include <stdexcept>
#include <algorithm>

TEST(MainAdditional, IntToStringAndStringToIntIdentity) {
    std::string alphabet = "abcdef1234";
    for (uint64_t num : {0ull, 1ull, 10ull, 123456789ull, (uint64_t)1<<63}) {
        std::string s = int_to_string(num, alphabet, 8);
        uint64_t restored = string_to_int(s, alphabet);
        EXPECT_EQ(restored, num);
    }
}

TEST(MainAdditional, EncodeAndDecodeRoundtrip) {
    auto uuid = ShortUUID().uuid();
    auto s = ShortUUID().encode(uuid);
    auto u2 = ShortUUID().decode(s);
    EXPECT_EQ(uuid, u2);
}

TEST(MainAdditional, GetAndSetAlphabet) {
    std::string alpha = "zyxwvutsrqponmlkjihgfedcba234567";
    set_alphabet(alpha);
    std::string got = get_alphabet();
    std::sort(got.begin(), got.end());
    std::string cpy = alpha; std::sort(cpy.begin(), cpy.end());
    EXPECT_EQ(got, cpy);
}

TEST(MainAdditional, RandomLength) {
    std::string rand1 = random(5);
    EXPECT_EQ(rand1.size(), 5);
}

TEST(MainAdditional, SetAlphabetInvalid) {
    ShortUUID s;
    EXPECT_THROW(s.set_alphabet("a", false), std::invalid_argument);
}

TEST(MainAdditional, ShortUUIDEncodeUuidTypeError) {
    ShortUUID shortuuid;
    EXPECT_THROW(shortuuid.encode("notauuid"), std::invalid_argument);
}

TEST(MainAdditional, ShortUUIDDecodeStrTypeError) {
    ShortUUID shortuuid;
    EXPECT_THROW(shortuuid.decode(12345), std::invalid_argument);
}

TEST(MainAdditional, PropertiesAndMethods) {
    ShortUUID s;
    EXPECT_GE(s.length(), 1);
    std::string alpha = s.get_alphabet();
    EXPECT_GT(alpha.size(), 0u);
}

TEST(MainAdditional, UUIDRandomAndNamed) {
    ShortUUID s;
    std::string anon = s.uuid();
    EXPECT_GT(anon.size(), 0u);

    std::string url_id = s.uuid("https://example.com");
    EXPECT_GT(url_id.size(), 0u);

    std::string dns_id = s.uuid("myname");
    EXPECT_GT(dns_id.size(), 0u);
}

TEST(MainAdditional, RandomMethod) {
    ShortUUID s;
    std::string r = s.random(6);
    EXPECT_EQ(r.size(), 6u);
}

TEST(MainAdditional, DecodeLegacyBehavior) {
    auto u = ShortUUID().uuid();
    auto enc = ShortUUID().encode(u);
    std::string rev = enc; std::reverse(rev.begin(), rev.end());
    auto u2 = ShortUUID().decode(rev, true);
    EXPECT_NE(u2, "");
}

TEST(MainAdditional, StringToIntInvalidChar) {
    std::string alpha = "abc";
    EXPECT_THROW(string_to_int("ad", alpha), std::invalid_argument);
}

TEST(MainAdditional, IntToStringWithPadding) {
    std::string alpha = "abcde12345";
    std::string s = int_to_string(5, alpha, 8);
    EXPECT_EQ(s.size(), 8u);
}

TEST(MainAdditional, SetAlphabetDontSort) {
    ShortUUID s("cba", true);
    EXPECT_EQ(s.get_alphabet(), "cba");
}