#include <gtest/gtest.h>
#include "shortuuid/shortuuid.h"
#include <string>
#include <stdexcept>

class LegacyShortUUIDTest : public ::testing::Test {};

TEST_F(LegacyShortUUIDTest, EncodingAndDecodingWithDefaultAlphabet) {
    std::string uuid = ShortUUID().uuid();
    ShortUUID s;
    std::string code = s.encode(uuid);
    EXPECT_EQ(s.decode(code), uuid);
    std::string code2 = encode(uuid);
    EXPECT_EQ(decode(code2), uuid);
}

TEST_F(LegacyShortUUIDTest, EncodingAndDecodingCustomAlphabet) {
    ShortUUID s("abcdefghijklmnopqrstuvw12345");
    std::string uuid = s.uuid();
    std::string code = s.encode(uuid);
    EXPECT_EQ(s.decode(code), uuid);
}

TEST_F(LegacyShortUUIDTest, InvalidDecodeRaises) {
    EXPECT_THROW({
        decode("!!!notvalid!!!");
    }, std::exception);
}

class TestShortUUIDClass : public ::testing::Test {};

TEST_F(TestShortUUIDClass, Roundtrip) {
    ShortUUID s;
    std::string uuid = s.uuid();
    std::string shrt = s.encode(uuid);
    EXPECT_EQ(s.decode(shrt), uuid);
}

TEST_F(TestShortUUIDClass, AlphabetSetterAndGetter) {
    ShortUUID s;
    std::string old = s.get_alphabet();
    std::string custom = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789abcdefghijkmnopqrstuvwxyz";
    s.set_alphabet(custom);
    std::string newalpha = s.get_alphabet();
    EXPECT_EQ(newalpha, custom);
    std::string really_custom = "abcdefghijklmnopqrstuvxyzABCDEFGHIJKLMNPQRSTUVWXYZ";
    s.set_alphabet(really_custom);
    EXPECT_NE(old, s.get_alphabet());

    ShortUUID s2(true);
    std::string original_alpha = "ZYXWVUTSRQPONMLKJHGFEDCBAabcdefghijkmnopqrstuvwxyz23456789";
    s2.set_alphabet(original_alpha, true);
    EXPECT_EQ(s2.get_alphabet(), original_alpha);
}

TEST_F(TestShortUUIDClass, SetAlphabetPreservesCustom) {
    ShortUUID s("ciao", true);
    EXPECT_EQ(s.get_alphabet(), "ciao");
}

TEST_F(TestShortUUIDClass, UuidArgumentStrTypeRaises) {
    ShortUUID s;
    EXPECT_THROW(s.encode(std::string("invalid-type")), std::invalid_argument);
}

TEST_F(TestShortUUIDClass, LegacyDefaultAlphabet) {
    ShortUUID s;
    std::string uuid = s.uuid();
    std::string enc = s.encode(uuid);
    std::string dec = s.decode(enc);
    EXPECT_EQ(uuid, dec);
}

TEST_F(TestShortUUIDClass, DecodeInvalidType) {
    ShortUUID s;
    int invalid = 12345;
    EXPECT_THROW(s.decode(invalid), std::exception);
}