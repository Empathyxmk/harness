#include <gtest/gtest.h>
#include "serializer.h"
#include <vector>

TEST(SerializerPublicTest, RoundtripPublic) {
    Serializer s("a_different_key");
    std::map<std::string, std::vector<int>> d{{"gamma", {13}}, {"zeta", {5,4}}};
    std::string token = s.dumps(d);
    EXPECT_FALSE(token.empty());
    EXPECT_EQ(s.loads(token), d);
}

TEST(SerializerPublicTest, RoundtripWithCustomSerializerPublic) {
    // You'd simulate this in C++ with custom (de)serializer object.
    // For demonstration, we skip custom separators logic in C++.
    Serializer s("k3y_public!");
    std::map<std::string, int> fooMap{{"foo", 100}};
    std::string token = s.dumps(fooMap);
    EXPECT_EQ(s.loads(token), fooMap);
}

TEST(SerializerPublicTest, InvalidPayloadPublic) {
    Serializer s("testkey");
    EXPECT_THROW({
        s.loads("$%anotherinvalidpayload$%");
    }, BadSignature);
}

TEST(SerializerPublicTest, BadSignaturePublic) {
    Serializer s("keyxxx");
    EXPECT_THROW({
        s.loads("totallyinvalidsignature-publictest");
    }, BadSignature);
}