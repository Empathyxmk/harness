#include <gtest/gtest.h>
#include "auth.hpp"
#include <string>

using namespace auth;

TEST(TestAuth, BasicAuth) {
    BasicAuth a("foo", "bar");
    auto hdrs = a.generate_headers();
    EXPECT_TRUE(hdrs.count("Authorization") > 0);
    EXPECT_TRUE(hdrs["Authorization"].find("Basic ") == 0);
}

TEST(TestAuth, CallSetsHeaders) {
    BasicAuth a("foo", "bar");
    DummyRequest req;
    a.attach(req);
    EXPECT_TRUE(req.headers.count("Authorization") > 0);
}

TEST(TestAuth, Repr) {
    BasicAuth ba("username", "pw");
    std::string rep = ba.repr();
    EXPECT_NE(rep.find("BasicAuth"), std::string::npos);
}

TEST(TestAuth, BearerToken) {
    BearerToken bt("tok123");
    auto hdrs = bt.generate_headers();
    EXPECT_EQ(hdrs["Authorization"], "Bearer tok123");
    DummyRequest req;
    bt.attach(req);
    EXPECT_TRUE(req.headers.count("Authorization") > 0);
}

TEST(TestAuth, ReprBearer) {
    BearerToken b("tk");
    EXPECT_NE(b.repr().find("BearerToken"), std::string::npos);
}

TEST(TestAuth, ApiKeyHeaderOnly) {
    ApiKey ak("mykey", "myval", true);
    auto hdrs = ak.generate_headers();
    EXPECT_TRUE(hdrs.count("mykey") > 0);
    DummyRequest req;
    ak.attach(req);
    EXPECT_TRUE(req.headers.count("mykey") > 0);
}

TEST(TestAuth, ApiKeyInQueryNotSupported) {
    ApiKey ak("qkey", "qval", false);
    auto hdrs = ak.generate_headers();
    EXPECT_TRUE(hdrs.empty());
}

TEST(TestAuth, ReprApiKey) {
    ApiKey ak("api", "value");
    EXPECT_NE(ak.repr().find("ApiKey"), std::string::npos);
}