#include <gtest/gtest.h>
#include "src/config.h"
#include <chrono>

using namespace flask_login_config;

TEST(PublicConfigTest, CookieNamePublic) {
    ASSERT_TRUE(COOKIE_NAME.find("remember") == 0);
}

TEST(PublicConfigTest, CookieDurationPublic) {
    auto days = std::chrono::duration_cast<std::chrono::hours>(COOKIE_DURATION).count() / 24;
    ASSERT_GE(days, 300);
}

TEST(PublicConfigTest, CookieSecurePublic) {
    ASSERT_FALSE(COOKIE_SECURE);
}

TEST(PublicConfigTest, CookieHttpOnlyPublic) {
    ASSERT_TRUE(COOKIE_HTTPONLY);
}

TEST(PublicConfigTest, CookieSameSitePublic) {
    // Default None mapped to empty string/null equivalent
    ASSERT_TRUE(COOKIE_SAMESITE.empty());
}

TEST(PublicConfigTest, LoginMessagePublic) {
    ASSERT_TRUE(LOGIN_MESSAGE.find("log in") != std::string::npos
        || LOGIN_MESSAGE.find("Log in") != std::string::npos);
}

TEST(PublicConfigTest, LoginMessageCategoryPublic) {
    ASSERT_TRUE(LOGIN_MESSAGE_CATEGORY.length() > 2);
}

TEST(PublicConfigTest, RefreshMessagePublic) {
    ASSERT_TRUE(REFRESH_MESSAGE.find("Please reauth") == 0);
}

TEST(PublicConfigTest, RefreshMessageCategoryPublic) {
    ASSERT_EQ(REFRESH_MESSAGE_CATEGORY, LOGIN_MESSAGE_CATEGORY);
}

TEST(PublicConfigTest, IdAttributePublic) {
    auto idx = ID_ATTRIBUTE.size();
    ASSERT_TRUE(ID_ATTRIBUTE.substr(idx-2) == "id" || ID_ATTRIBUTE.substr(idx-3) == "_id");
}

TEST(PublicConfigTest, SessionKeysPublic) {
    ASSERT_TRUE(SESSION_KEYS.count("_user_id"));
    ASSERT_TRUE(SESSION_KEYS.count("_id"));
}

TEST(PublicConfigTest, ExemptMethodsPublic) {
    ASSERT_TRUE(EXEMPT_METHODS.count("OPTIONS"));
}

TEST(PublicConfigTest, UseSessionForNextPublic) {
    ASSERT_FALSE(USE_SESSION_FOR_NEXT);
}