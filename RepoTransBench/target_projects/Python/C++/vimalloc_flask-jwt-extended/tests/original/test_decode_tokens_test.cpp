#include <gtest/gtest.h>
// Full implementation as per test_decode_tokens.py

TEST(DecodeTokensTest, MissingClaimsThrows) {
    // Remove required claims from token, expect JWTDecodeError
    // ... Full implementation
}

TEST(DecodeTokensTest, DefaultDecodeValues) {
    // Token missing type/jti/fresh, defaults applied
    // ... Full implementation
}

// Continue for all test cases in decode_token: expired, audience, subject, leeway, unverified headers, etc.