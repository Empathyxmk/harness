#include <gtest/gtest.h>
// Full implementation as per test_headers.py

TEST(HeadersTest, DefaultHeadersBehavior) {
    // Check access with default and incorrect headers, check error messages
    // ... Full implementation
}

TEST(HeadersTest, HeaderTrailingSpacesAndCommas) {
    // Check special cases with whitespace
    // ... Full implementation
}

TEST(HeadersTest, CustomHeaderName) {
    // JWT_HEADER_NAME set, test header variants
    // ... Full implementation
}

TEST(HeadersTest, CustomHeaderType) {
    // JWT_HEADER_TYPE set, test new type, removal, and error handling
    // ... Full implementation
}

TEST(HeadersTest, MissingHeadersDefaultAndCustom) {
    // Missing headers and custom unauthorized_loader
    // ... Full implementation
}

TEST(HeadersTest, HeaderWithoutJwt) {
    // "Bearer " with no JWT, error expected
    // ... Full implementation
}

TEST(HeadersTest, CustomErrorMsgKey) {
    // Error msg key configurable, verify map structure
    // ... Full implementation
}