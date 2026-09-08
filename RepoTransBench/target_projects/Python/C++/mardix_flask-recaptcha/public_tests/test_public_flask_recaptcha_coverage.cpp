#include <gtest/gtest.h>
#include "flask_recaptcha.h"

using namespace mardix;

TEST(PublicCoverage, DefaultsAreDifferent) {
    DEFAULTS &defaults = DEFAULTS::getInstance();
    EXPECT_TRUE(defaults.ssl_verify);
    EXPECT_FALSE(defaults.SIZE.empty());
}

TEST(PublicCoverage, RecaptchaInitialConfig) {
    // Simulate a config
    std::map<std::string, std::string> config = {
        {"RECAPTCHA_SITE_KEY", "publicUnique123"},
        {"RECAPTCHA_SECRET_KEY", "publicSecretABC"}
    };
    ReCaptcha recaptcha(config["RECAPTCHA_SITE_KEY"], config["RECAPTCHA_SECRET_KEY"]);
    recaptcha.setParams("theme", "light");
    recaptcha.setParams("size", "compact");

    EXPECT_EQ(recaptcha.site_key(), "publicUnique123");
    EXPECT_EQ(recaptcha.secret_key(), "publicSecretABC");
    EXPECT_EQ(recaptcha.getParam("theme"), "light");
    EXPECT_EQ(recaptcha.getParam("size"), "compact");
}