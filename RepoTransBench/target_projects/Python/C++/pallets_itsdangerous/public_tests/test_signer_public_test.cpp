#include <gtest/gtest.h>
#include "signer.h"

TEST(SignerPublicTest, RoundtripPublic) {
    Signer s("random_key_public");
    std::vector<uint8_t> value{'p','u','b','l','i','c','-','t','e','s','t','-','v','a','l','u','e'};
    auto signedval = s.sign(value);
    EXPECT_FALSE(signedval.empty());
    EXPECT_EQ(s.unsign(signedval), value);
}
TEST(SignerPublicTest, SeparatorPublic) {
    Signer s("another_key", ".");
    std::vector<uint8_t> val{'m','y','v','a','l','u','e'};
    auto signedval = s.sign(val);
    EXPECT_NE(std::find(signedval.begin(), signedval.end(), '.'), signedval.end());
    EXPECT_EQ(s.unsign(signedval), val);
}
TEST(SignerPublicTest, BadSignaturePublic) {
    Signer s("public_sign");
    std::vector<uint8_t> badval{'b','a','d','l','y','s','i','g','n','e','d','v','a','l','u','e','.','p','u','b','l','i','c','s','i','g'};
    EXPECT_THROW({
        s.unsign(badval);
    }, BadSignature);
}
TEST(SignerPublicTest, KeyRotationPublic) {
    std::vector<std::string> keys = {"old_secret_public", "new_secret_public"};
    Signer s(keys);
    std::vector<uint8_t> value{'r','o','t','a','t','e','s','t','u','f','f'};
    auto signedval = s.sign(value);
    EXPECT_EQ(s.unsign(signedval), value);
}