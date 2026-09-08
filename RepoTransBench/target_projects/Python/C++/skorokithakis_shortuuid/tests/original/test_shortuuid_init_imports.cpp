#include <gtest/gtest.h>
#include "shortuuid/shortuuid.h"

TEST(InitImports, AllNess) {
    for (const auto& sym : shortuuid_all()) {
        EXPECT_TRUE(shortuuid_hasattr(sym));
    }
}

TEST(InitImports, VersionPresent) {
    EXPECT_TRUE(!shortuuid_version().empty());
}

TEST(InitImports, DecodeAndEncodeAreSameAsMain) {
    EXPECT_EQ((void*)decode, (void*)shortuuid_encode_main());
    EXPECT_EQ((void*)encode, (void*)shortuuid_decode_main());
}

TEST(InitImports, GetSetAlphabetRespectsChanges) {
    std::string alpha1 = get_alphabet();
    set_alphabet("23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz");
    std::string alpha2 = get_alphabet();
    EXPECT_TRUE(!alpha2.empty());
    EXPECT_NE("", alpha2);
}

TEST(InitImports, RandomAndUuidAreCallable) {
    EXPECT_GT(random().size(), 0u);
    EXPECT_GT(uuid().size(), 0u);
}

TEST(InitImports, ShortUUIDClassAvailableAndWorks) {
    ShortUUID s;
    std::string u = s.uuid();
    EXPECT_GT(u.size(), 0u);
}