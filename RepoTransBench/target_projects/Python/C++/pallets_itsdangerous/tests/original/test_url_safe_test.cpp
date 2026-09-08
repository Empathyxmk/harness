#include <gtest/gtest.h>
#include "url_safe_serializer.h"  // You must provide C++ implementation

TEST(URLSafeSerializerTest, Roundtrip) {
    URLSafeSerializer s("urlsecret");
    std::map<std::string, std::string> data{{"k", "v"}};
    std::string token = s.dumps(data);
    EXPECT_FALSE(token.empty());
    EXPECT_EQ(s.loads(token), data);
}

TEST(URLSafeSerializerTest, Separators) {
    URLSafeSerializer s("secret", "mysalt");
    std::map<std::string, int> data{{"x", 100}};
    std::string token = s.dumps(data);
    EXPECT_FALSE(token.empty());
    EXPECT_EQ(s.loads(token), data);
}

TEST(URLSafeSerializerTest, BadSignature) {
    URLSafeSerializer s("othersecret");
    EXPECT_THROW({
        s.loads("badbadbad");
    }, BadSignature);
}

TEST(URLSafeSerializerTest, ReturnPayload) {
    URLSafeSerializer s("secret");
    std::map<std::string, int> data{{"val", 4}};
    std::string token = s.dumps(data);
    EXPECT_EQ(s.loads(token, /*return_payload=*/true), data);
}