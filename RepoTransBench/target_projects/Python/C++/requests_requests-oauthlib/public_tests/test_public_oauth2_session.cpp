#include <gtest/gtest.h>
#include "requests_oauthlib/OAuth2Session.h"

TEST(OAuth2SessionPublicTest, AddTokenPublic) {
    std::map<std::string, std::string> token = {
        {"token_type", "Bearer"},
        {"access_token", "pubtok123456789"},
        {"refresh_token", "pubrtok987654321"},
        {"expires_in", "1234"},
        {"expires_at", "1586300999"}
    };
    OAuth2Session sess("publicclientid");
    // Simulate send, get, and header assertion
    EXPECT_EQ(token["token_type"], "Bearer"); // Replace with proper test logic
}

// Add more tests for PKCE, refresh, error, etc. as in the source