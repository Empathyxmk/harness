#include <gtest/gtest.h>
#include "timed_serializer.h"
#include <chrono>
#include <thread>

TEST(TimedSerializerTest, DumpsLoads) {
    TimedSerializer s("secret-key");
    std::map<std::string, std::string> data{{"msg","timed"}};
    std::string dumped = s.dumps(data);
    auto loaded = s.loads(dumped);
    EXPECT_EQ(loaded, data);
}

TEST(TimedSerializerTest, Expiry) {
    TimedSerializer s("secret-expiry");
    std::map<std::string, int> data{{"foo",1}};
    std::string token = s.dumps(data);
    EXPECT_EQ(s.loads(token), data);
    EXPECT_THROW({
        s.loads(token, /*max_age=*/-1);  // simulate expired
    }, SignatureExpired);
}

TEST(TimedSerializerTest, TupleLoadingOptions) {
    TimedSerializer s("secret-key2");
    std::string token = s.dumps({{"a", 2}});
    auto result = s.loads_with_timestamp(token);
    EXPECT_EQ(result.first, std::map<std::string, int>{{"a",2}});
    // Accept float or datetime (simulate as double timestamp)
    EXPECT_GT(result.second, 0.0);
}

TEST(TimedSerializerTest, BadSignature) {
    TimedSerializer s("secret");
    EXPECT_THROW({
        s.loads("bad-token");
    }, BadSignature);

    std::string orig = s.dumps({{"foo", 42}});
    std::string tampered(orig.rbegin(), orig.rend());
    EXPECT_THROW({
        s.loads(tampered);
    }, BadTimeSignature);
}