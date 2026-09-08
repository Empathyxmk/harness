#include <gtest/gtest.h>
#include "onetimepass/onetimepass.h"
#include <string>
#include <vector>

using namespace onetimepass;

TEST(PublicOnetimepassExtra, SecretToBase32) {
    std::vector<uint8_t> secret{'d','i','f','f','e','r','e','n','t',' ','s','e','c','r','e','t'};
    std::string b32 = secret_to_base32(secret);
    EXPECT_EQ(typeid(b32), typeid(std::string));
    for (char c : b32) {
        if (c == '=') continue;
        EXPECT_NE(std::string("ABCDEFGHIJKLMNOPQRSTUVWXYZ234567").find(c), std::string::npos);
    }
}

TEST(PublicOnetimepassExtra, ValidBase32ReturnTypes) {
    EXPECT_TRUE(valid_base32("MFRGGZDFMZRW63LQ"));
    EXPECT_FALSE(valid_base32("123#XYZ"));
}

TEST(PublicOnetimepassExtra, GenerateNewSecretLength) {
    std::string secret8 = generate_new_secret(8);
    std::string secret24 = generate_new_secret(24);
    EXPECT_EQ(secret8.length(), 8);
    EXPECT_EQ(secret24.length(), 24);
}

TEST(PublicOnetimepassExtra, GenerateNewSecretBase32) {
    std::string secret = generate_new_secret(18);
    EXPECT_TRUE(valid_base32(secret));
}