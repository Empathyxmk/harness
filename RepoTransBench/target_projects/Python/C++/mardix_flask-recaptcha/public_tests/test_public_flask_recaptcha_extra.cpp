#include <gtest/gtest.h>
#include "flask_recaptcha.h"

using namespace mardix;

TEST(PublicReCaptchaExtra, HtmlGenerationDifferent) {
    ReCaptcha recaptcha;
    recaptcha.site_key("pub-key-test");
    std::string html = recaptcha.get_code();
    EXPECT_NE(html.find("pub-key-test"), std::string::npos);
    EXPECT_NE(html.find("g-recaptcha"), std::string::npos);
}

TEST(PublicReCaptchaExtra, ThemeInHtml) {
    ReCaptcha recaptcha;
    recaptcha.site_key("test-key");
    recaptcha.theme("dark");
    std::string html = recaptcha.get_code();
    EXPECT_NE(html.find("data-theme=\"dark\""), std::string::npos);
}