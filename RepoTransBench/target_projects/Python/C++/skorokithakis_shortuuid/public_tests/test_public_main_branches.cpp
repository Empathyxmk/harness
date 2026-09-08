#include <gtest/gtest.h>
#include "shortuuid/shortuuid.h"
#include <string>
#include <algorithm>

TEST(PublicMainBranches, ShortUUIDDifferentAlphabetBranch) {
    ShortUUID sq("mnop5678");
    auto shortval = sq.random(4);
    EXPECT_EQ(shortval.size(), 4u);
    EXPECT_TRUE(std::all_of(shortval.begin(), shortval.end(), [](char c){
        std::string allowed = "mnop5678";
        return allowed.find(c) != std::string::npos;
    }));
}

TEST(PublicMainBranches, ShortUUIDEmptyAlphabetRaises) {
    EXPECT_THROW({
        ShortUUID sq("");
    }, std::invalid_argument);
}

TEST(PublicMainBranches, ShortUUIDRandomSameLength) {
    ShortUUID sq;
    auto s1 = sq.random(6);
    auto s2 = sq.random(6);
    EXPECT_EQ(s1.size(), 6u);
    EXPECT_EQ(s2.size(), 6u);
}

TEST(PublicMainBranches, ShortUUIDEncodeDecodeSpecial) {
    ShortUUID sq;
    std::string uuid = "11111111-2222-3333-4444-555555555555";
    auto encoded = sq.encode(uuid);
    auto decoded = sq.decode(encoded);
    EXPECT_EQ(uuid, decoded);
}

TEST(PublicMainBranches, ShortUUIDCopyInstance) {
    ShortUUID orig("azAZQW12");
    ShortUUID copy(orig.get_alphabet());
    EXPECT_EQ(orig.get_alphabet(), copy.get_alphabet());
}