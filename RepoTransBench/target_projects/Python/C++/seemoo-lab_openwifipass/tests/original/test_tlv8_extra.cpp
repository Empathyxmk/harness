#include <gtest/gtest.h>
#include <vector>
#include <map>
#include <string>
#include "lib/TLV8.h"

TEST(TLV8BoxExtra, EncodeDecodeStrAndToDict) {
    // Compose TLV8 instance, encode, decode
    TLV8 tlv(0x01, {0xAA, 0xBB});
    std::vector<uint8_t> encoded = tlv.encode();
    TLV8Box box = TLV8Box::decodeFromData(encoded);
    ASSERT_EQ(typeid(box), typeid(TLV8Box));
    ASSERT_FALSE(box.tlv8s.empty());
    const TLV8& decoded = box.tlv8s[0];
    EXPECT_EQ(decoded.type_, 0x01);
    EXPECT_EQ(decoded.payload, std::vector<uint8_t>({0xAA, 0xBB}));
    EXPECT_TRUE(tlv.toString().find("TLV8(type: 1") == 0);
    EXPECT_TRUE(box.toString().length() > 0);
    std::map<int, std::vector<uint8_t>> dct = box.toDict();
    ASSERT_TRUE(dct.find(0x01) != dct.end());
    EXPECT_EQ(dct[0x01], std::vector<uint8_t>({0xAA, 0xBB}));
}


TEST(TLV8BoxExtra, MultipleEntriesToDictMerging) {
    TLV8 t1(7, {0x01});
    TLV8 t2(7, {0x02});
    TLV8Box box({t1, t2});
    std::map<int, std::vector<uint8_t>> dct = box.toDict();
    ASSERT_TRUE(dct.count(7));
    EXPECT_EQ(dct[7], std::vector<uint8_t>({0x01, 0x02}));
}

TEST(TLV8BoxExtra, DecodeFromDataBoundary) {
    {
        std::vector<uint8_t> data = {0x22}; // not enough length
        TLV8Box box = TLV8Box::decodeFromData(data);
        ASSERT_EQ(typeid(box), typeid(TLV8Box));
        EXPECT_EQ(box.tlv8s.size(), 0);
    }
    {
        std::vector<uint8_t> data = {0x22, 0x01}; // no payload present
        TLV8Box box = TLV8Box::decodeFromData(data);
        ASSERT_EQ(typeid(box), typeid(TLV8Box));
        EXPECT_EQ(box.tlv8s.size(), 0);
    }
}

TEST(TLV8BoxExtra, EmptyEncode) {
    TLV8Box box({});
    EXPECT_EQ(box.encode(), std::vector<uint8_t>());
    EXPECT_TRUE(box.toString().size() >= 0);
}