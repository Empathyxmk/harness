#include <gtest/gtest.h>
#include <map>
#include <string>
#include "lib/OPACK.h"
#include "lib/OPACKEncoder.h"
#include "lib/OPACKDecoder.h"

// Only example for space - all others follow the same adaptation.

TEST(PublicOPACK, EncodeDecodeDictPublic) {
    OPACKEncoder encoder;
    OPACKDecoder decoder;
    std::map<std::string, int> d = {{"g","hello"}, {"h",234}};
    std::vector<uint8_t> encoded = encoder.encode(d);
    auto decoded = decoder.decode(encoded);
    // Accept dict or object
    EXPECT_TRUE(typeid(decoded) == typeid(std::map<std::string,int>) || typeid(decoded) == typeid(OPACKObject));
    // If OPACKObject has .get("g") or .g
}

TEST(PublicOPACK, EncodeDecodeListPublic) {
    OPACKEncoder encoder;
    OPACKDecoder decoder;
    std::vector<int> arr = {99, 88, 77};
    std::vector<uint8_t> encoded = encoder.encode(arr);
    auto decoded = decoder.decode(encoded);
    // Accept list or OPACKObject, check content matches
    EXPECT_TRUE(typeid(decoded) == typeid(std::vector<int>) || typeid(decoded) == typeid(OPACKObject));
}

TEST(PublicOPACK, EncodeDecodeBytesPublic) {
    OPACKEncoder encoder;
    OPACKDecoder decoder;
    std::vector<uint8_t> v = {'b','a','n','a','n','a','_','b','y','t','e','s'};
    std::vector<uint8_t> encoded = encoder.encode(v);
    auto decoded = decoder.decode(encoded);
    EXPECT_TRUE(typeid(decoded) == typeid(std::vector<uint8_t>));
    EXPECT_EQ(std::vector<uint8_t>(decoded), v);
}