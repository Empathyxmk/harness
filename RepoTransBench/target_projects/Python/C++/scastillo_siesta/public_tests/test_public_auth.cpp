#include <gtest/gtest.h>
#include "auth.hpp"
#include <string>

using namespace auth;

TEST(TestAuthPublic, BasicAuth) {
    BasicAuth a("alice", "wonderland");
    auto hdrs = a.generate_headers();
    EXPECT_TRUE(hdrs.count("Authorization") > 0);
    EXPECT_TRUE(hdrs["Authorization"].find("Basic ") == 0);
}

TEST(TestAuthPublic, CallSetsHeaders) {
    BasicAuth a("alice", "wonderland");
    DummyRequest req;
    a.attach(req);
    EXPECT_TRUE(req.headers.count("Authorization") > 0);
}

TEST(TestAuthPublic, Repr) {
    BasicAuth ba("someone", "secret");
    std::string rep = ba.repr();
    EXPECT_NE(rep.find("BasicAuth"), std::string::npos);
}

TEST(TestAuthPublic, BearerToken) {
    BearerToken bt("publictoken456");
    auto hdrs = bt.generate_headers();
    EXPECT_EQ(hdrs["Authorization"], "Bearer publictoken456");
    DummyRequest req;
    bt.attach(req);
    EXPECT_TRUE(req.headers.count("Authorization") > 0);
}

TEST(TestAuthPublic, ReprBearer) {
    BearerToken b("pubtoken");
    EXPECT_NE(b.repr().find("BearerToken"), std::string::npos);
}

TEST(TestAuthPublic, ApiKeyHeaderOnly) {
    ApiKey ak("pubkey", "pubval", true);
    auto hdrs = ak.generate_headers();
    EXPECT_TRUE(hdrs.count("pubkey") > 0);
    DummyRequest req;
    ak.attach(req);
    EXPECT_TRUE(req.headers.count("pubkey") > 0);
}

TEST(TestAuthPublic, ApiKeyInQueryNotSupported) {
    ApiKey ak("querykey", "queryval", false);
    auto hdrs = ak.generate_headers();
    EXPECT_TRUE(hdrs.empty());
}

TEST(TestAuthPublic, ReprApiKey) {
    ApiKey ak("pubapi", "pubvalue");
    EXPECT_NE(ak.repr().find("ApiKey"), std::string::npos);
}