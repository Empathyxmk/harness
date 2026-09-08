#include <gtest/gtest.h>
#include <map>
#include <string>
#include <vector>
#include <set>
#include "lib/OPACK.h"

// We assume OPACKEncoder and OPACKDecoder classes are defined and functional in C++,
// with `encode` and `decode` methods matching python method signatures.
// Exception class below for error testing. Adjust class names as per your codebase if they differ.

TEST(OPACKExtra, EncodeDecodeSimple) {
    OPACKEncoder encoder;
    OPACKDecoder decoder;
    std::map<std::string, int> d = {{"a", 123}, {"b", 456}};
    std::vector<uint8_t> encoded = encoder.encode(d);
    std::map<std::string, int> decoded = decoder.decode(encoded);
    // Accept either a map or object-like return
    EXPECT_EQ(decoded, d);
}

TEST(OPACKExtra, DecoderError) {
    OPACKDecoder decoder;
    // Malformed input should throw exception
    std::vector<uint8_t> bad_data = {0x99, 0x99, 0x99};
    EXPECT_THROW({
        decoder.decode(bad_data);
    }, std::exception);
}

TEST(OPACKExtra, EncoderError) {
    OPACKEncoder encoder;
    // Encoding an unsupported type like set should throw
    std::set<int> s = {1, 2, 3};
    EXPECT_THROW({
        encoder.encode(s);
    }, std::exception);
}