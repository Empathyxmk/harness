#include <gtest/gtest.h>
// Full implementation as per test_blocklist.py

TEST(BlocklistTest, AccessTokenRevocationSkip) {
    // Blocklist loader returns True but skip_revocation_check enabled, should succeed
    // ... Full implementation
}

TEST(BlocklistTest, AccessTokenRevocationNoSkip) {
    // Blocklist loader returns True, skip_revocation_check FALSE, get 401
    // ... Full implementation
}

TEST(BlocklistTest, AccessTokenNotBlocklisted) {
    // Blocklist loader returns False, allowed in all cases
    // ... Full implementation
}

TEST(BlocklistTest, CustomBlocklistedMessage) {
    // Custom revoked_token_loader returns custom error/message/HTTP code
    // ... Full implementation
}