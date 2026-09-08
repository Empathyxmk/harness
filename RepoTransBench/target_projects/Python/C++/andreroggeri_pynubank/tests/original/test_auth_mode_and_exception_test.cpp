#include <gtest/gtest.h>
#include "pynubank/auth_mode.h"
#include "pynubank/exception.h"

// Example test: Replace implementation with real translation of Python test logic.

TEST(AuthModeTest, ThrowsOnInvalidMode) {
    try {
        AuthMode m = AuthMode::FromString("NOT_A_MODE");
        (void)m;
        FAIL() << "Expected InvalidAuthModeException";
    } catch(const InvalidAuthModeException& e) {
        EXPECT_STREQ(e.what(), "Invalid authentication mode: NOT_A_MODE");
    } catch(...) {
        FAIL() << "Expected InvalidAuthModeException";
    }
}

TEST(ExceptionTest, HasCorrectMessage) {
    NubankException ex("test error message");
    EXPECT_STREQ(ex.what(), "test error message");
}