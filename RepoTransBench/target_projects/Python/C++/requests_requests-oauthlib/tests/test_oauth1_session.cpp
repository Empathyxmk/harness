#include <gtest/gtest.h>
#include "requests_oauthlib/OAuth1.h"
#include <string>
#include <map>

TEST(OAuth1SessionTest, FetchRequestToken) {
    OAuth1Session session("foo", "secret");
    std::string url = "https://example.com/token";
    session.set_token({{"oauth_token", "fake-key"}, {"oauth_token_secret", "fake-secret"}, {"oauth_verifier", "fake-verifier"}});
    auto token = session.get_token();
    EXPECT_EQ(token["oauth_token"], "fake-key");
    EXPECT_EQ(token["oauth_token_secret"], "fake-secret");

    // Add fake/mock response logic as needed for fetch_request_token
}

TEST(OAuth1SessionTest, AuthorizedFalse) {
    OAuth1Session session("foo");
    EXPECT_FALSE(session.authorized());
}

// Additional tests: non-ascii, query/body signature, header auth, PLAINTEXT, RSA, etc.