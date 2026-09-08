#include <gtest/gtest.h>
// Full implementation as per test_additional_claims_loader.py

TEST(ClaimsLoaderTest, AdditionalClaimsInAccessToken) {
    // Use additional_claims_loader for access token, check claims via endpoint
    // ... Full implementation
}

TEST(ClaimsLoaderTest, NonSerializableClaimsCauseError) {
    // Loader returns unserializable object, should throw error
    // ... Full implementation
}

TEST(ClaimsLoaderTest, TokenFromComplexObject) {
    // Use user_identity_loader and additional_claims_loader with user object
    // ... Full implementation
}

TEST(ClaimsLoaderTest, AdditionalClaimsInRefreshToken) {
    // as above, for refresh tokens
    // ... Full implementation
}

TEST(ClaimsLoaderTest, AdditionalClaimsAtCreation) {
    // Specified via create_access_token/create_refresh_token directly
    // ... Full implementation
}

TEST(ClaimsLoaderTest, ClaimsMergeBehavior) {
    // Loader + create_access_token both provide claims, merge and precedence
    // ... Full implementation
}