#include <gtest/gtest.h>
#include <thread>
#include <semaphore>
#include "babel_flask_babel/Babel.h"

// (Assuming an RAII class BabelForceLocale for context management.)

TEST(TestForceLocale, ForceLocale) {
    BabelApp app;
    Babel b(&app, [](){ return "de_DE"; });
    BabelRequestContext ctx(app);
    EXPECT_EQ(b.get_locale(), "de_DE");
    {
        BabelForceLocale force_locale("en_US");
        EXPECT_EQ(b.get_locale(), "en_US");
    }
    EXPECT_EQ(b.get_locale(), "de_DE");
}

TEST(TestForceLocale, ForceLocaleWithThreading) {
    BabelApp app;
    Babel b(&app, [](){ return "de_DE"; });

    std::counting_semaphore<> semaphore(0);

    auto first_request = [&]() {
        BabelRequestContext ctx(app);
        BabelForceLocale force_locale("en_US");
        EXPECT_EQ(b.get_locale(), "en_US");
        semaphore.acquire();
    };

    std::thread t1(first_request);

    {
        BabelRequestContext ctx(app);
        EXPECT_EQ(b.get_locale(), "de_DE");
    }
    semaphore.release();
    t1.join();
}

TEST(TestForceLocale, ForceLocaleWithThreadingAndAppContext) {
    BabelApp app;
    Babel b(&app, [](){ return "de_DE"; });

    std::counting_semaphore<> semaphore(0);

    auto first_app_context = [&]() {
        BabelAppContext ctx(app);
        BabelForceLocale force_locale("en_US");
        EXPECT_EQ(b.get_locale(), "en_US");
        semaphore.acquire();
    };

    std::thread t1(first_app_context);

    {
        BabelAppContext ctx(app);
        EXPECT_EQ(b.get_locale(), "de_DE");
    }
    semaphore.release();
    t1.join();
}

TEST(TestForceLocale, RefreshDuringForceLocale) {
    BabelApp app;
    Babel b(&app, [](){ return "de_DE"; });
    BabelRequestContext ctx(app);
    {
        BabelForceLocale force_locale("en_US");
        EXPECT_EQ(b.get_locale(), "en_US");
        b.refresh();
        EXPECT_EQ(b.get_locale(), "en_US");
    }
}