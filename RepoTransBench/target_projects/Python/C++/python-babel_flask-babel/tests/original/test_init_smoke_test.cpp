#include <gtest/gtest.h>
#include <string>
#include <map>
#include "babel_flask_babel/Babel.h"

class DummyApp {
public:
    std::map<std::string, std::string> config;
    std::map<std::string, BabelConfiguration*> extensions;
};

TEST(TestInitSmoke, BabelInitAndAppProperties) {
    DummyApp app;
    Babel babel;
    babel.init_app(&app);
    BabelConfiguration* config = app.extensions["babel"];
    ASSERT_TRUE(config != nullptr);
    EXPECT_EQ(config->default_locale, "en");
    EXPECT_EQ(config->default_domain, "messages");
    EXPECT_TRUE(config->translation_directories.size() > 0);
    EXPECT_TRUE(config->instance == &babel);
}

TEST(TestInitSmoke, BabelInitAppConfigOptionsOverride) {
    DummyApp app;
    app.config["BABEL_DEFAULT_LOCALE"] = "fr";
    app.config["BABEL_DOMAIN"] = "customdomain";
    app.config["BABEL_TRANSLATION_DIRECTORIES"] = "foo;bar";
    Babel babel;
    babel.init_app(&app);
    BabelConfiguration* config = app.extensions["babel"];
    EXPECT_EQ(config->default_locale, "fr");
    EXPECT_EQ(config->default_domain, "customdomain");
    ASSERT_EQ(config->default_directories.size(), 2u);
    EXPECT_EQ(config->default_directories[0], "foo");
    EXPECT_EQ(config->default_directories[1], "bar");
}

TEST(TestInitSmoke, BabelInitAppWithSelectors) {
    DummyApp app;
    auto selector = [](){ return std::string("de"); };
    Babel babel;
    babel.init_app(&app, selector, selector);
    BabelConfiguration* config = app.extensions["babel"];
    EXPECT_EQ(config->locale_selector(), "de");
    EXPECT_EQ(config->timezone_selector(), "de");
}

TEST(TestInitSmoke, GetBabel) {
    DummyApp app;
    Babel babel;
    babel.init_app(&app);
    BabelConfiguration* config = get_babel(&app);
    ASSERT_TRUE(config != nullptr);
    ASSERT_THROW(get_babel(nullptr), std::runtime_error); // Should throw when current app not set
}

TEST(TestInitSmoke, DefaultDateFormatsDefined) {
    Babel babel;
    auto d = babel.default_date_formats;
    ASSERT_TRUE(!d.empty());
    EXPECT_EQ(d.at("datetime"), "medium");
}