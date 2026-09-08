#include <gtest/gtest.h>
#include "requests_oauthlib/OAuth2.h"

TEST(TestPublicOAuth2, PublicOAuth2AuthHeaderDiffData) {
    std::map<std::string, std::string> token = {
        {"access_token", "tok_9876543210abc"},
        {"token_type", "Bearer"},
        {"expires_in", "600"}
    };
    OAuth2 oauth("public_client_id", token);
    std::string req = "GET /";
    std::string out = oauth(req);
    EXPECT_TRUE(out.find("Bearer tok_9876543210abc") != std::string::npos);
}

TEST(TestPublicOAuth2, PublicOAuth2AuthReprDiff) {
    OAuth2 oauth("public_id");
    std::string rep = oauth.repr();
    EXPECT_TRUE(rep.find("public_id") != std::string::npos);
    EXPECT_TRUE(rep.find("OAuth2(") == 0);
}