#include <gtest/gtest.h>
#include <string>
#include <map>
#include "babel_flask_babel/Babel.h"

TEST(TestPublicIntegration, NoRequestContext) {
    Babel b;
    BabelApp app;
    b.init_app(&app);
    {
        BabelAppContext ctx(app);
        EXPECT_TRUE(b.get_translations().is_null());
    }
}

TEST(TestPublicIntegration, MultipleDirectories) {
    Babel b;
    BabelApp app;
    app.config["BABEL_TRANSLATION_DIRECTORIES"] = "translations;renamed_translations";
    app.config["BABEL_DEFAULT_LOCALE"] = "ja";
    b.init_app(&app);
    {
        BabelRequestContext ctx(app);
        auto translations = b.list_translations();
        EXPECT_TRUE(translations.size() == 3 || translations.size() == 4);
        EXPECT_TRUE(translations[0] == "de" || translations[0] == "ja");
        EXPECT_EQ(b.gettext("Good morning, %(who)s!", {{"who","Anna"}}), "Good morning, Anna!");
    }
}

TEST(TestPublicIntegration, MultipleDirectoriesMultipleDomains) {
    Babel b;
    BabelApp app;
    app.config["BABEL_TRANSLATION_DIRECTORIES"] = "renamed_translations;translations_different_domain";
    app.config["BABEL_DEFAULT_LOCALE"] = "de_DE";
    app.config["BABEL_DOMAIN"] = "myapp;messages";
    b.init_app(&app);
    {
        BabelRequestContext ctx(app);
        auto translations = b.list_translations();
        ASSERT_EQ(translations.size(), 3u);
        EXPECT_EQ(translations[1], "de");
        EXPECT_EQ(b.gettext("Thank you"), "Thank you");
        EXPECT_EQ(b.gettext("See you"), "See you");
    }
}

TEST(TestPublicIntegration, MultipleDirectoriesDifferentDomain) {
    Babel b;
    BabelApp app;
    app.config["BABEL_TRANSLATION_DIRECTORIES"] = "translations_different_domain;renamed_translations";
    app.config["BABEL_DEFAULT_LOCALE"] = "de_DE";
    app.config["BABEL_DOMAIN"] = "myapp";
    b.init_app(&app);
    {
        BabelRequestContext ctx(app);
        auto translations = b.list_translations();
        ASSERT_EQ(translations.size(), 3u);
        EXPECT_EQ(translations[2], "de_DE");
        EXPECT_EQ(b.gettext("Farewell"), "Farewell");
        EXPECT_EQ(b.gettext("Bonjour"), "Bonjour");
    }
}

TEST(TestPublicIntegration, DifferentDomain) {
    Babel b;
    BabelApp app;
    app.config["BABEL_TRANSLATION_DIRECTORIES"] = "translations_different_domain";
    app.config["BABEL_DEFAULT_LOCALE"] = "de_DE";
    app.config["BABEL_DOMAIN"] = "myapp";
    b.init_app(&app);
    {
        BabelRequestContext ctx(app);
        auto translations = b.list_translations();
        ASSERT_EQ(translations.size(), 2u);
        EXPECT_EQ(translations[1], "de_DE");
        EXPECT_EQ(b.gettext("Salut"), "Salut");
    }
}

TEST(TestPublicIntegration, LazyOldStyleFormatting) {
    auto lazy_string = BabelLazyGettext("Good morning, %(user)s");
    EXPECT_EQ(lazy_string % std::map<std::string, std::string>{{"user", "Sophie"}}, "Good morning, Sophie");

    auto lazy_string2 = BabelLazyGettext("bonjour");
    EXPECT_EQ("Good day: " + (std::string)lazy_string2, "Good day: bonjour");
}

#include <sstream>
TEST(TestPublicIntegration, LazyPickling) {
    auto lazy_string = BabelLazyGettext("Bar");
    std::ostringstream oss;
    oss << lazy_string.value();
    std::istringstream iss(oss.str());
    std::string loaded;
    iss >> loaded;
    EXPECT_EQ(loaded, lazy_string.value());
}