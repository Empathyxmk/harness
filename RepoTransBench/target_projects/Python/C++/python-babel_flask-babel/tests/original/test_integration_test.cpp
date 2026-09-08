#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <map>
#include "babel_flask_babel/Babel.h"

// See note on the stub implementation in previous test.

TEST(TestIntegration, NoRequestContextGivesNullTranslations) {
    Babel b;
    BabelApp app;
    b.init_app(&app);

    {
        BabelAppContext appctx(app);
        // get_translations() returns NullTranslations if outside of request context
        EXPECT_TRUE(b.get_translations().is_null());
    }
}

TEST(TestIntegration, MultipleDirectories) {
    Babel b;
    BabelApp app;

    app.config["BABEL_TRANSLATION_DIRECTORIES"] = "translations;renamed_translations";
    app.config["BABEL_DEFAULT_LOCALE"] = "de_DE";
    b.init_app(&app);

    {
        BabelRequestContext ctx(app);
        std::vector<std::string> translations = b.list_translations();
        ASSERT_TRUE(translations.size() == 4);
        EXPECT_EQ(translations[0], "de");
        EXPECT_EQ(translations[1], "ja");
        EXPECT_EQ(translations[2], "de");
        EXPECT_EQ(translations[3], "de_DE");
        EXPECT_EQ(b.gettext("Hello %(name)s!", {{"name","Peter"}}), "Hallo Peter!");
    }
}

TEST(TestIntegration, MultipleDirectoriesMultipleDomains) {
    Babel b;
    BabelApp app;

    app.config["BABEL_TRANSLATION_DIRECTORIES"] = "renamed_translations;translations_different_domain";
    app.config["BABEL_DEFAULT_LOCALE"] = "de_DE";
    app.config["BABEL_DOMAIN"] = "messages;myapp";
    b.init_app(&app);

    {
        BabelRequestContext ctx(app);
        auto translations = b.list_translations();
        ASSERT_TRUE(translations.size() == 3);
        EXPECT_EQ(translations[0], "de");
        EXPECT_EQ(translations[1], "de");
        EXPECT_EQ(translations[2], "de_DE");
        EXPECT_EQ(b.gettext("Hello %(name)s!", {{"name","Peter"}}), "Hallo Peter!");
        EXPECT_EQ(b.gettext("Good bye"), "Auf Wiedersehen");
    }
}

TEST(TestIntegration, MultipleDirectoriesDifferentDomain) {
    Babel b;
    BabelApp app;
    app.config["BABEL_TRANSLATION_DIRECTORIES"] = "translations_different_domain;renamed_translations";
    app.config["BABEL_DEFAULT_LOCALE"] = "de_DE";
    app.config["BABEL_DOMAIN"] = "myapp";
    b.init_app(&app);

    {
        BabelRequestContext ctx(app);
        auto translations = b.list_translations();
        ASSERT_TRUE(translations.size() == 3);
        EXPECT_EQ(translations[0], "de");
        EXPECT_EQ(translations[1], "de");
        EXPECT_EQ(translations[2], "de_DE");
        EXPECT_EQ(b.gettext("Hello %(name)s!", {{"name","Peter"}}), "Hallo Peter!");
        EXPECT_EQ(b.gettext("Good bye"), "Auf Wiedersehen");
    }
}

TEST(TestIntegration, DifferentDomain) {
    Babel b;
    BabelApp app;
    app.config["BABEL_TRANSLATION_DIRECTORIES"] = "translations_different_domain";
    app.config["BABEL_DEFAULT_LOCALE"] = "de_DE";
    app.config["BABEL_DOMAIN"] = "myapp";
    b.init_app(&app);

    {
        BabelRequestContext ctx(app);
        auto translations = b.list_translations();
        ASSERT_TRUE(translations.size() == 2);
        EXPECT_EQ(translations[0], "de");
        EXPECT_EQ(translations[1], "de_DE");
        EXPECT_EQ(b.gettext("Good bye"), "Auf Wiedersehen");
    }
}

TEST(TestIntegration, LazyOldStyleFormatting) {
    auto lazy_string = BabelLazyGettext("Hello %(name)s");
    EXPECT_EQ(lazy_string % std::map<std::string, std::string>{{"name", "test"}}, "Hello test");
    auto lazy_string2 = BabelLazyGettext("test");
    EXPECT_EQ("Hello " + (std::string)lazy_string2, "Hello test");
}

#include <sstream>

TEST(TestIntegration, LazyPickling) {
    auto lazy_string = BabelLazyGettext("Foo");
    // Simulate "pickling": serialize and deserialize. Replace with your own serialization logic.
    std::ostringstream oss;
    oss << lazy_string.value();
    std::istringstream iss(oss.str());
    std::string loaded;
    iss >> loaded;
    // Simulate that the value survived serialization
    EXPECT_EQ(loaded, lazy_string.value());
}