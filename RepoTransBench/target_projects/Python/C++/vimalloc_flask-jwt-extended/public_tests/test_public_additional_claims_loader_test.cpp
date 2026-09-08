#include <gtest/gtest.h>
// Include your JWT/mock server helpers

TEST(PublicAdditionalClaimsLoader, ClaimsAreIncluded) {
    // Setup mock app with claims loader returning "role":"editor", "active":false
    // Generate token, send GET request with token header using test client
    // Assert status 200 and response body contains expected keys/values
    // ... FULL IMPLEMENTATION required
}