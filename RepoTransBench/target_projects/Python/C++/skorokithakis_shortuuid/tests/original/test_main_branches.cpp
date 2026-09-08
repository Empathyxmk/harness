#include <gtest/gtest.h>
#include "shortuuid/shortuuid.h"

TEST(MainBranches, IntToStringZeroAndEmpty) {
    std::string alphabet = "abcd";
    EXPECT_EQ(int_to_string(0, alphabet, 5), "aaaaa");
}

TEST(MainBranches, IntToStringShortPadding) {
    std::string alphabet = "abc";
    EXPECT_EQ(int_to_string(2, alphabet, 1), "c");
}

TEST(MainBranches, DecodeLegacyTrueBehavior) {
    ShortUUID s;
    std::string uuid = s.uuid();
    std::string enc = s.encode(uuid);
    std::string rev = enc;
    std::reverse(rev.begin(), rev.end());
    std::string u_dec = s.decode(rev, true);
    EXPECT_FALSE(u_dec.empty());
}

TEST(MainBranches, SetAlphabetDontSortPreservedOrder) {
    ShortUUID s("ACBXYZ", true);
    EXPECT_EQ(s.get_alphabet(), "ACBXYZ");
}

TEST(MainBranches, SetAlphabetErrors) {
    ShortUUID s;
    EXPECT_THROW(s.set_alphabet("z", true), std::invalid_argument);
    EXPECT_THROW(s.set_alphabet(std::vector<char>{}, true), std::invalid_argument);
}