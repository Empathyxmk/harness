#include <gtest/gtest.h>
#include "overholt/settings.h"

TEST(PublicSettingsTest, SettingsPublicValues) {
    EXPECT_GE(strlen(Overholt::Settings::SECRET_KEY), 8);
    EXPECT_TRUE(typeid(Overholt::Settings::SECRET_KEY) == typeid(const char*));
    EXPECT_TRUE(typeid(Overholt::Settings::DEBUG) == typeid(bool));
    EXPECT_TRUE(typeid(Overholt::Settings::SECURITY_SEND_REGISTER_EMAIL) == typeid(bool));
}