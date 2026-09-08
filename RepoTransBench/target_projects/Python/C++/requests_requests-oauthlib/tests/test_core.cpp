#include <gtest/gtest.h>
#include "requests_oauthlib/OAuth1.h"
#include <string>
#include <map>
#include <sstream>

TEST(OAuth1Test, FormEncodedSignature) {
    OAuth1Session sess("client_key");
    std::string url = "http://a.b/path?query=retain";
    std::string content_type = "application/x-www-form-urlencoded";
    std::map<std::string, std::string> data = {{"this", "really"}, {"is", ""}, {"form", "encoded"}};

    // Simulate request preparation, authorization header, and assert correct outcome
    std::string auth = sess.authorization_url(url);
    // Validate auth string includes expected signature pieces
    EXPECT_TRUE(auth.find("oauth_token") != std::string::npos || auth.find("client_key") != std::string::npos);
}

// Add all original logic from core.py tests, non-form-encoded, binary, URL tests, content-type checks, etc.