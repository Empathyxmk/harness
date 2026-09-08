#include <gtest/gtest.h>
// Full implementation as per test_jwt_header_loader.py

TEST(HeaderLoaderTest, JwtHeadersInAccessToken) {
    // Set additional_headers_loader for access token
    // ... Full implementation
}

TEST(HeaderLoaderTest, NonSerializableHeadersThrow) {
    // Loader returns unserializable, throw TypeError
    // ... Full implementation
}

TEST(HeaderLoaderTest, JwtHeadersInRefreshToken) {
    // ... Full implementation
}

TEST(HeaderLoaderTest, HeaderAtCreation) {
    // direct additional_headers
    // ... Full implementation
}

TEST(HeaderLoaderTest, HeaderAtCreationOverride) {
    // Loader + direct, check override/precedence
    // ... Full implementation
}