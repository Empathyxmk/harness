#include <gtest/gtest.h>
#include "timed_serializer.h"
#include <thread>
#include <chrono>

TEST(TimedSerializerPublicTest, RoundtripPublic) {
    TimedSerializer s("pubtimedkey");
    std::map<std::string,int> data{{"index", 333}};
    std::string token = s.dumps(data);
    EXPECT_FALSE(token.empty());
    EXPECT_EQ(s.loads(token), data);
}

TEST(TimedSerializerPublicTest, WithMaxAgePublic) {
    TimedSerializer s("pubtimedkey");
    std::map<std::string,int> data{{"val", 17}};
    std::string token = s.dumps(data);
    EXPECT_EQ(s.loads(token, 3), data);
}

TEST(TimedSerializerPublicTest, BadSignaturePublic) {
    TimedSerializer s("pubk2");
    EXPECT_THROW({
        s.loads("definitely_invalid_token");
    }, BadSignature);
}

TEST(TimedSerializerPublicTest, SignatureExpiredPublic) {
    TimedSerializer s("expirepub");
    std::map<std::string, bool> data{{"test", true}};
    std::string token = s.dumps(data);
    std::this_thread::sleep_for(std::chrono::seconds(1));
    EXPECT_THROW({
        s.loads(token, 0);
    }, SignatureExpired);
}