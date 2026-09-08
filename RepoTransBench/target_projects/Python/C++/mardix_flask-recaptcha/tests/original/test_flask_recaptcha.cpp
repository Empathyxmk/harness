#include <gtest/gtest.h>
#include "flask_recaptcha.h"

using namespace mardix;

struct FakeResponse {
    bool success;
    FakeResponse(bool s) : success(s) {}
};

TEST(ReCaptchaOriginal, InitWithDefaultArgs) {
    ReCaptcha r;
    EXPECT_TRUE(r.is_enabled());
}

TEST(ReCaptchaOriginal, SiteKeyAndSecretKey) {
    ReCaptcha r("abc", "def");
    EXPECT_EQ(r.site_key(), "abc");
    EXPECT_EQ(r.secret_key(), "def");
}

TEST(ReCaptchaOriginal, ThemeAndTypeProperty) {
    ReCaptcha r;
    EXPECT_FALSE(r.theme().empty()); // Should have a default
    EXPECT_FALSE(r.type().empty());
}

TEST(ReCaptchaOriginal, SetParamsMethodExists) {
    ReCaptcha r;
    r.setParams("a", "1");
    r.setParams("b", "2");
    EXPECT_EQ(r.getParam("a"), "1");
    EXPECT_EQ(r.getParam("b"), "2");
}

TEST(ReCaptchaOriginal, ValidateSuccess) {
    ReCaptcha r("a", "b", true);
    EXPECT_TRUE(r.verify("SOME", "HOST"));
}

TEST(ReCaptchaOriginal, ValidateFail) {
    ReCaptcha r("a", "b", true);
    EXPECT_FALSE(r.verify("WRONG", "HOST"));
}

TEST(ReCaptchaOriginal, VerifyException) {
    ReCaptcha r("a", "b", true);
    // C++ version: simulate an exception-throwing backend unavailable by custom code not coverage here
    // Not applicable in this dummy since we have direct logic
    EXPECT_FALSE(r.verify("", "FAILHOST"));
}

TEST(ReCaptchaOriginal, DisabledByFlag) {
    ReCaptcha r;
    r.is_enabled(false);
    EXPECT_TRUE(r.verify("ANY", "X"));
}

TEST(ReCaptchaOriginal, ReprAndStr) {
    ReCaptcha r("public", "topsecret", true);
    EXPECT_FALSE(r.repr().empty());
    EXPECT_FALSE(r.str().empty());
}