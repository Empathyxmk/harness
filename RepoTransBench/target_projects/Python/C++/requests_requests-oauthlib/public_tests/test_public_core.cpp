#include <gtest/gtest.h>
#include "requests_oauthlib/core.h"
#include <string>
#include <map>

class DummySession {
public:
    std::map<std::string, std::string> token;
};

TEST(PublicCoreTest, SetTokenPublicDiffToken) {
    DummySession sess;
    set_token(sess, {{"access_token", "unicorn_xyz"}, {"token_type", "Bearer"}});
    EXPECT_EQ(sess.token["access_token"], "unicorn_xyz");
    EXPECT_EQ(sess.token["token_type"], "Bearer");
}

TEST(PublicCoreTest, SetTokenPublicOtherDiff) {
    DummySession sess;
    set_token(sess, {{"access_token", "golden_public_token"}, {"token_type", "macaroons"}});
    EXPECT_EQ(sess.token["access_token"], "golden_public_token");
}