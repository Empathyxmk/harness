#include <gtest/gtest.h>
#include <string>
#include <map>
#include "babel_flask_babel/Babel.h"

TEST(TestAppFactory, AppFactoryWorks) {
    Babel b;

    auto locale_selector = []() { return std::string("de_DE"); };

    auto create_app = [&]() {
        BabelApp app;
        b.init_app(&app, "en_US", locale_selector);
        return app;
    };

    BabelApp app = create_app();
    BabelRequestContext ctx(app);
    EXPECT_EQ(b.get_locale(), "de_DE");
    EXPECT_EQ(b.gettext("Hello %(name)s!", {{"name", "Peter"}}), "Hallo Peter!");
}