#include <gtest/gtest.h>
#include "src/config.h"

using namespace flask_login_config;

TEST(ConfigTest, ConfigValues) {
    EXPECT_EQ(COOKIE_NAME, "remember_token");
    // days==365
    auto days = std::chrono::duration_cast<std::chrono::hours>(COOKIE_DURATION).count() / 24;
    EXPECT_EQ(days, 365);
    EXPECT_EQ(COOKIE_SECURE, false);
    EXPECT_EQ(COOKIE_HTTPONLY, true);
    EXPECT_TRUE(EXEMPT_METHODS.count("OPTIONS") == 1);
    EXPECT_EQ(LOGIN_MESSAGE, "Please log in to access this page.");
    EXPECT_EQ(LOGIN_MESSAGE_CATEGORY, "message");
    EXPECT_EQ(REFRESH_MESSAGE, "Please reauthenticate to access this page.");
    EXPECT_EQ(REFRESH_MESSAGE_CATEGORY, "message");
    EXPECT_EQ(ID_ATTRIBUTE, "get_id");
    EXPECT_TRUE(SESSION_KEYS.count("_user_id"));
    EXPECT_TRUE(SESSION_KEYS.count("_remember"));
    EXPECT_EQ(USE_SESSION_FOR_NEXT, false);
}