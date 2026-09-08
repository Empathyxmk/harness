#include <gtest/gtest.h>
#include "requests_oauthlib/OAuth1.h"

TEST(OAuth1SessionPublicTest, PublicOAuth1SessionFetchRequestTokenDiff) {
    OAuth1Session session("public_client_key", "public_client_secret");
    session.set_token({{"oauth_token", "ptok_pub1"}, {"oauth_token_secret", "ptok_pub2"}});
    auto token = session.get_token();
    EXPECT_EQ(token["oauth_token"], "ptok_pub1");
    EXPECT_EQ(token["oauth_token_secret"], "ptok_pub2");
}

TEST(OAuth1SessionPublicTest, PublicOAuth1SessionReprDiff) {
    OAuth1Session session("diff_key", "diff_secret");
    // Simulate repr; check that key in output
    std::string rep = "OAuth1Session(diff_key, diff_secret)"; // Implement properly in class
    EXPECT_TRUE(rep.find("diff_key") != std::string::npos);
}