#include <gtest/gtest.h>
#include <string>
#include <map>
#include "babel_flask_babel/Babel.h"

class DummyAppPublic {
public:
    std::map<std::string, std::string> config;
    std::map<std::string, BabelConfiguration*> extensions;
};

TEST(TestPublicInitSmoke, BabelInitAndAppProperties) {
    DummyAppPublic app;
    Babel babel;
    babel.init_app(&app);
    BabelConfiguration* config = app.extensions["babel"];
    ASSERT_TRUE(config != nullptr);
    EXPECT_EQ(config->default_locale, "en");
    EXPECT_EQ(config->default_domain, "messages");
    EXPECT_TRUE(config->translation_directories.size() > 0);
    EXPECT_TRUE(config->instance == &babel);
}

TEST(TestPublicInitSmoke, BabelInitAppConfigOptionsOverride) {
    DummyAppPublic app;
    app.config["BABEL_DEFAULT_LOCALE"] = "es";
    app.config["BABEL_DOMAIN"] = "alt_domain";
    app.config["BABEL_TRANSLATION_DIRECTORIES"] = "alpha;beta";
    Babel babel;
    babel.init_app(&app);
    BabelConfiguration* config = app.extensions["babel"];
    EXPECT_EQ(config->default_locale, "es");
    EXPECT_EQ(config->default_domain, "alt_domain");
    ASSERT_EQ(config->default_directories.size(), 2u);
    EXPECT_EQ(config->default_directories[0], "alpha");
    EXPECT_EQ(config->default_directories[1], "beta");
}

TEST(TestPublicInitSmoke, BabelInitAppWithSelectors) {
    DummyAppPublic app;
    auto selector = [](){ return std::string("it"); };
    Babel babel;
    babel.init_app(&app, selector, selector);
    BabelConfiguration* config = app.extensions["babel"];
    EXPECT_EQ(config->locale_selector(), "it");
    EXPECT_EQ(config->timezone_selector(), "it");
}

TEST(TestPublicInitSmoke, GetBabel) {
    DummyAppPublic app;
    Babel babel;
    babel.init_app(&app);
    BabelConfiguration* config = get_babel(&app);
    ASSERT_TRUE(config != nullptr);
    ASSERT_THROW(get_babel(nullptr), std::runtime_error);
}

TEST(TestPublicInitSmoke, DefaultDateFormatsDefined) {
    Babel babel;
    auto d = babel.default_date_formats;
    ASSERT_TRUE(!d.empty());
    EXPECT_EQ(d.at("date"), "medium");
}