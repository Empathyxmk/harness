#include <gtest/gtest.h>
#include "pynubank/auth_mode.h"
#include "pynubank/exception.h"

// Example: Public test case for AuthMode
TEST(PublicAuthModeTest, ValidMode) {
    AuthMode m = AuthMode::FromString("password");
    EXPECT_EQ(m.getMode(), "password");
}

TEST(PublicExceptionTest, ThrowsOnCustom) {
    EXPECT_THROW(throw NubankException("fail"), NubankException);
}