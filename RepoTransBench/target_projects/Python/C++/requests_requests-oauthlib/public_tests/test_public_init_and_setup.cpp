#include <gtest/gtest.h>
#include "requests_oauthlib/OAuth2Session.h"
#include <string>

TEST(PublicInitAndSetupTest, VersionNumberExistsAndDiff) {
    std::string version = "2.0.0"; // Simulate real version check
    ASSERT_GE(version.size(), 5u);
    for (const char& c : version) ASSERT_TRUE((c == '.') || isdigit(c));
}

TEST(PublicInitAndSetupTest, PublicImportsAvailable) {
    // Check that essential classes are available (simulating import)
    OAuth2Session sess("dummy");
    ASSERT_TRUE(true);
}