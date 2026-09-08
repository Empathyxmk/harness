#include <gtest/gtest.h>
#include "flask_recaptcha.h"

using namespace mardix;

TEST(PublicReCaptcha, SetAndGetSiteKey) {
    ReCaptcha recaptcha;
    recaptcha.site_key("different_public_key");
    EXPECT_EQ(recaptcha.site_key(), "different_public_key");
}

TEST(PublicReCaptcha, SetAndGetSecretKey) {
    ReCaptcha recaptcha;
    recaptcha.secret_key("different_public_secret");
    EXPECT_EQ(recaptcha.secret_key(), "different_public_secret");
}

TEST(PublicReCaptcha, LanguageSetterAndGetter) {
    ReCaptcha recaptcha;
    recaptcha.language("fr");
    EXPECT_EQ(recaptcha.language(), "fr");
}

TEST(PublicReCaptcha, ThemeSetterAndGetter) {
    ReCaptcha recaptcha;
    recaptcha.theme("dark");
    EXPECT_EQ(recaptcha.theme(), "dark");
}