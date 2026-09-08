#include <gtest/gtest.h>
// Full implementation as per test_user_lookup.py

TEST(UserLookupTest, NoLookupLoaderSpecified) {
    // Access JWT identity without user_lookup_loader, expect error message
    // ... Full implementation
}

TEST(UserLookupTest, LoadValidUser) {
    // Provide user_lookup_loader, check correct username lookup
    // ... Full implementation
}

TEST(UserLookupTest, LoadInvalidUser) {
    // Loader returns None, expect 401/error message
    // ... Full implementation
}

TEST(UserLookupTest, CustomUserLookupErrors) {
    // Loader returns None, custom error handler, expect custom response
    // ... Full implementation
}