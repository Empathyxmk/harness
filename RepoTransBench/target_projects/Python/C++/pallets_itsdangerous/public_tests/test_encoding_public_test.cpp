#include <gtest/gtest.h>
#include "encoding.h"

TEST(EncodingPublicTest, WantBytesTypeCoercionPublic) {
    EXPECT_EQ(want_bytes(std::vector<uint8_t>{'x','y','z'}), std::vector<uint8_t>{'x','y','z'});
    EXPECT_EQ(want_bytes(std::string("hello")), std::vector<uint8_t>{'h','e','l','l','o'});
    EXPECT_EQ(want_bytes(std::vector<uint8_t>{'t','e','s','t'}), std::vector<uint8_t>{'t','e','s','t'});
}
TEST(EncodingPublicTest, Base64RoundtripPublic) {
    std::vector<uint8_t> raw{'b','a','z','q','u','x'};
    std::string encoded = base64_encode(raw);
    std::vector<uint8_t> decoded = base64_decode(encoded);
    EXPECT_EQ(decoded, raw);
}
TEST(EncodingPublicTest, Base64DecodeErrorPublic) {
    EXPECT_THROW({
        base64_decode("??=", "raise");
    }, std::exception);
}