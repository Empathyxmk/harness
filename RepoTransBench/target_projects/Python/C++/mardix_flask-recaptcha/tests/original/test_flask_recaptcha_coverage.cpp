#include <gtest/gtest.h>
#include "flask_recaptcha.h"

using namespace mardix;

struct DummyApp {
    std::map<std::string, std::string> config;
    std::function<std::map<std::string, std::string>()> _proc;

    DummyApp() {
        config = {
            {"RECAPTCHA_SITE_KEY", "site"},
            {"RECAPTCHA_SECRET_KEY", "secret"},
            {"RECAPTCHA_ENABLED", "true"},
            {"RECAPTCHA_THEME", "dark"},
            {"RECAPTCHA_TYPE", "audio"},
            {"RECAPTCHA_SIZE", "compact"},
            {"RECAPTCHA_LANGUAGE", "fr"},
            {"RECAPTCHA_TABINDEX", "3"}
        };
    }

    void context_processor(std::function<std::map<std::string, std::string>()> fn) {
        _proc = fn;
    }
};

TEST(ReCaptchaCoverage, GetCodeVarious) {
    ReCaptcha r("k", "s", true);
    std::string code = r.get_code();
    EXPECT_NE(code.find("<script"), std::string::npos);
    EXPECT_NE(code.find("k"), std::string::npos);

    ReCaptcha r2("k", "s", false);
    std::string code2 = r2.get_code();
    EXPECT_EQ(code2, "");
}

TEST(ReCaptchaCoverage, InitAppCodeRegistration) {
    // Simulate context_processor. In real Flask, context processor returns dict of variables
    DummyApp app;
    ReCaptcha r;
    // Simulate registration
    app.context_processor([&]() {
        std::map<std::string, std::string> ctxt;
        ctxt["recaptcha"] = r.get_code();
        return ctxt;
    });
    auto cdict = app._proc();
    ASSERT_TRUE(cdict.find("recaptcha") != cdict.end());
    EXPECT_NE(cdict["recaptcha"].find("g-recaptcha"), std::string::npos);
}

TEST(ReCaptchaCoverage, DefaultsClassProperties) {
    DEFAULTS &def = DEFAULTS::getInstance();
    EXPECT_EQ(def.THEME, "light");
    EXPECT_EQ(def.TYPE, "image");
    EXPECT_EQ(def.SIZE, "normal");
    EXPECT_EQ(def.LANGUAGE, "en");
    EXPECT_EQ(def.TABINDEX, 0);
}

TEST(ReCaptchaCoverage, ReprAndStrNoError) {
    ReCaptcha r("x", "y");
    EXPECT_FALSE(r.repr().empty());
    EXPECT_FALSE(r.str().empty());
}

TEST(ReCaptchaCoverage, InitWithAppOnly) {
    DummyApp app;
    ReCaptcha r(app.config["RECAPTCHA_SITE_KEY"], app.config["RECAPTCHA_SECRET_KEY"],
                app.config["RECAPTCHA_THEME"], app.config["RECAPTCHA_TYPE"],
                app.config["RECAPTCHA_SIZE"], app.config["RECAPTCHA_LANGUAGE"],
                std::stoi(app.config["RECAPTCHA_TABINDEX"]),
                app.config["RECAPTCHA_ENABLED"] == "true");
    EXPECT_EQ(r.site_key(), "site");
    EXPECT_EQ(r.secret_key(), "secret");
    EXPECT_EQ(r.theme(), "dark");
    EXPECT_EQ(r.type(), "audio");
    EXPECT_EQ(r.size(), "compact");
    EXPECT_EQ(r.language(), "fr");
    EXPECT_EQ(r.tabindex(), 3);
}

TEST(ReCaptchaCoverage, VerifyReturnsTrueIfDisabled) {
    ReCaptcha r("test", "test", false);
    EXPECT_TRUE(r.verify("stuff", "127.0.0.1"));
}

TEST(ReCaptchaCoverage, VerifyNetworkFailure) {
    // Simulate API failure: response always false if not "SOME"
    ReCaptcha r("a", "b", true);
    EXPECT_FALSE(r.verify("bla", "ip"));
}