#include <gtest/gtest.h>
#include "overholt/settings.h"

TEST(SettingsTest, SettingsValues) {
    // These values are expected to be defined in overholt/settings.h
    EXPECT_TRUE(Overholt::Settings::DEBUG);
    EXPECT_STREQ(Overholt::Settings::SECRET_KEY, "super-secret-key");
    EXPECT_FALSE(Overholt::Settings::SECURITY_SEND_REGISTER_EMAIL);
}