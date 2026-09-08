#include <gtest/gtest.h>
#include "babel_flask_babel/Babel.h"

TEST(TestPublicForceLocale, ContextManager) {
    BabelApp app;
    Babel b(&app);
    BabelRequestContext ctx(app);
    {
        BabelForceLocale force_locale("it");
        EXPECT_EQ(b.get_locale(), "it");
    }
    EXPECT_EQ(b.get_locale(), "en");
}

TEST(TestPublicForceLocale, NestedForceLocale) {
    BabelApp app;
    Babel b(&app, "fr");
    BabelRequestContext ctx(app);
    {
        BabelForceLocale force_locale1("ja");
        EXPECT_EQ(b.get_locale(), "ja");
        {
            BabelForceLocale force_locale2("de");
            EXPECT_EQ(b.get_locale(), "de");
        }
        EXPECT_EQ(b.get_locale(), "ja");
    }
    EXPECT_EQ(b.get_locale(), "fr");
}