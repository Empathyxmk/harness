#include <gtest/gtest.h>
#include <string>
#include "babel_flask_babel/Babel.h"

// This is a stub and must be adjusted according to your implementation.
// You should provide a Babel implementation that mimics the Flask Babel logic.

TEST(TestMultipleApps, HandlesMultipleFlaskApps) {
    Babel b;

    // App1: set to de_DE
    BabelApp app1;
    b.init_app(&app1, "de_DE");

    // App2: set to en_US
    BabelApp app2;
    b.init_app(&app2, "en_US");

    {
        BabelRequestContext ctx(app1); // Will need to implement a context for testing
        EXPECT_EQ(b.get_locale(), "de_DE");
        EXPECT_EQ(b.gettext("Hello %(name)s!", {{"name", "Peter"}}), "Hallo Peter!");
    }
    {
        BabelRequestContext ctx(app2);
        EXPECT_EQ(b.get_locale(), "en_US");
        EXPECT_EQ(b.gettext("Hello %(name)s!", {{"name", "Peter"}}), "Hello Peter!");
    }
}