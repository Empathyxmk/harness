#include <gtest/gtest.h>
#include "babel_flask_babel/Babel.h"

TEST(TestPublicAppFactory, BabelWithAppFactory) {
    auto create_app = [](std::map<std::string, std::string> config = {}) {
        BabelApp app;
        for (const auto& kv : config) app.config[kv.first] = kv.second;
        Babel b(&app);
        return app;
    };

    BabelApp app = create_app({{"BABEL_DEFAULT_LOCALE", "es"}});
    BabelRequestContext ctx(app);
    EXPECT_EQ(Babel::get_locale(), "es");
}

TEST(TestPublicAppFactory, BabelFactoryDeferredInit) {
    std::vector<int> created;
    auto my_selector = [&created](){ created.push_back(100); return std::string("fr"); };
    Babel b;
    BabelApp app;
    b.init_app(&app, my_selector);
    BabelRequestContext ctx(app);
    EXPECT_EQ(Babel::get_locale(), "fr");
    ASSERT_EQ(created.size(), 1u);
    EXPECT_EQ(created[0], 100);
}