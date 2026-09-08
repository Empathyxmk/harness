#include <gtest/gtest.h>
#include <string>
// #include "auth.h"

// Super-simplified
std::string secret_hash(const std::string& secret) {
    return std::string(secret.rbegin(), secret.rend()) + "encoded!";
}
bool check_encoded_secret(const std::string& candidate, const std::string& encoded) {
    return secret_hash(candidate) == encoded;
}

TEST(PublicAuthTest, SecretHashAndCheckPublic) {
    std::string secret = "another_secret_string";
    std::string encoded = secret_hash(secret);
    EXPECT_TRUE(!encoded.empty());
    EXPECT_EQ(encoded.find(secret), std::string::npos);
    EXPECT_TRUE(check_encoded_secret(secret, encoded));
    EXPECT_FALSE(check_encoded_secret("wrong_public_secret", encoded));
}