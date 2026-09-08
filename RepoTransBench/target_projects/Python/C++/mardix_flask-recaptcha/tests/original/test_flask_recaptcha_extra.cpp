#include <gtest/gtest.h>
#include "flask_recaptcha.h"

using namespace mardix;

TEST(ReCaptchaExtra, ParamsInit) {
    ReCaptcha r("A", "B", "light", "image", "compact", "en", 1, true);
    EXPECT_EQ(r.site_key(), "A");
    EXPECT_EQ(r.secret_key(), "B");
    EXPECT_EQ(r.theme(), "light");
    EXPECT_EQ(r.type(), "image");
    EXPECT_EQ(r.size(), "compact");
    EXPECT_EQ(r.language(), "en");
    EXPECT_EQ(r.tabindex(), 1);
}

TEST(ReCaptchaExtra, EnabledProperty) {
    ReCaptcha r("X", "Y", "light", "image", "normal", "en", 1, true);
    EXPECT_TRUE(r.is_enabled());
    ReCaptcha r2("X", "Y", "light", "image", "normal", "en", 1, false);
    EXPECT_FALSE(r2.is_enabled());
}

TEST(ReCaptchaExtra, GetCodeReturnsString) {
    ReCaptcha r("something", "else");
    std::string code = r.get_code();
    EXPECT_FALSE(code.empty());
}

TEST(ReCaptchaExtra, VerifyEmptyResponseToken) {
    ReCaptcha r("a", "b", true);
    EXPECT_FALSE(r.verify("", "host"));
}

TEST(ReCaptchaExtra, InitAppWithMinimum) {
    // Simulate only with site_key and secret_key
    struct App {
        std::map<std::string, std::string> config;
        std::function<std::map<std::string, std::string>()> _proc;
        App() {
            config = {
                {"RECAPTCHA_SITE_KEY", "k"},
                {"RECAPTCHA_SECRET_KEY", "s"}
            };
        }
        void context_processor(std::function<std::map<std::string, std::string>()> fn) {
            _proc = fn;
        }
    };
    App app;
    ReCaptcha r(app.config["RECAPTCHA_SITE_KEY"], app.config["RECAPTCHA_SECRET_KEY"]);
    app.context_processor([&]() {
        std::map<std::string, std::string> c;
        c["recaptcha"] = r.get_code();
        return c;
    });
    auto c = app._proc();
    EXPECT_TRUE(c.find("recaptcha") != c.end());
    EXPECT_FALSE(c["recaptcha"].empty());
}