#include <gtest/gtest.h>
#include "url_safe_serializer.h"

TEST(URLSafeSerializerPublicTest, RoundtripPublic) {
    URLSafeSerializer s("urlsecretpublic");
    std::map<std::string, std::string> data{{"foo", "bar"}};
    std::string token = s.dumps(data);
    EXPECT_FALSE(token.empty());
    EXPECT_EQ(s.loads(token), data);
}

TEST(URLSafeSerializerPublicTest, SeparatorsPublic) {
    URLSafeSerializer s("publicsecret", "othersalt");
    std::map<std::string, int> data{{"y", 303}};
    std::string token = s.dumps(data);
    EXPECT_FALSE(token.empty());
    EXPECT_EQ(s.loads(token), data);
}

TEST(URLSafeSerializerPublicTest, BadSignaturePublic) {
    URLSafeSerializer s("newsecret");
    EXPECT_THROW({
        s.loads("notavalidtoken");
    }, BadSignature);
}

TEST(URLSafeSerializerPublicTest, ReturnPayloadPublic) {
    URLSafeSerializer s("differentsecret");
    std::map<std::string, int> val{{"val", 7}};
    std::string token = s.dumps(val);
    EXPECT_EQ(s.loads(token, true), val);
}