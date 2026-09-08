#include <gtest/gtest.h>
#include "encoding.h"  // Implement want_bytes, base64_encode, base64_decode

TEST(EncodingTest, WantBytesTypeCoercion) {
    EXPECT_EQ(want_bytes(std::vector<uint8_t>{'a','b','c'}), std::vector<uint8_t>{'a','b','c'});
    EXPECT_EQ(want_bytes(std::string("abc")), std::vector<uint8_t>{'a','b','c'});
    EXPECT_EQ(want_bytes(std::vector<uint8_t>{'z','z','z'}), std::vector<uint8_t>({'z','z','z'}));
}

TEST(EncodingTest, Base64Roundtrip) {
    std::vector<uint8_t> raw{'f','o','o','b','a','r'};
    std::string encoded = base64_encode(raw);
    std::vector<uint8_t> decoded = base64_decode(encoded);
    EXPECT_EQ(decoded, raw);
}

TEST(EncodingTest, Base64DecodeError) {
    EXPECT_THROW({
        base64_decode("!!!", /*error=*/"raise");
    }, std::exception);
}