#include <gtest/gtest.h>
#include "babel_flask_babel/Babel.h"

TEST(TestPublicMultipleApps, MultipleApps) {
    Babel b;
    BabelApp app1; b.init_app(&app1, "fr_FR");
    BabelApp app2; b.init_app(&app2, "it_IT");
    {
        BabelRequestContext ctx(app1);
        EXPECT_EQ(b.get_locale(), "fr_FR");
        EXPECT_EQ(b.gettext("Welcome %(user)s!", {{"user", "Marie"}}), "Welcome Marie!");
    }
    {
        BabelRequestContext ctx(app2);
        EXPECT_EQ(b.get_locale(), "it_IT");
        EXPECT_EQ(b.gettext("Welcome %(user)s!", {{"user", "Luca"}}), "Welcome Luca!");
    }
}