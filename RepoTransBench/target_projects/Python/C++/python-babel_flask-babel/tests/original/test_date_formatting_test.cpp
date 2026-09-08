#include <gtest/gtest.h>
#include <string>
#include <map>
#include "babel_flask_babel/Babel.h"

TEST(TestDateFormatting, Basics) {
    BabelApp app;
    Babel b(&app);
    BabelDateTime d(2010, 4, 12, 13, 46);
    BabelTimeDelta delta = BabelTimeDelta::days(6);

    {
        BabelRequestContext ctx(app);
        EXPECT_EQ(b.format_datetime(d), "Apr 12, 2010, 1:46:00\u202fPM");
        EXPECT_EQ(b.format_date(d), "Apr 12, 2010");
        EXPECT_EQ(b.format_time(d), "1:46:00\u202fPM");
        EXPECT_EQ(b.format_timedelta(delta), "1 week");
        EXPECT_EQ(b.format_timedelta(delta, 1), "6 days");
    }
    {
        BabelRequestContext ctx(app);
        b.get_babel(&app)->default_timezone = "Europe/Vienna";
        EXPECT_EQ(b.format_datetime(d), "Apr 12, 2010, 3:46:00\u202fPM");
        EXPECT_EQ(b.format_date(d), "Apr 12, 2010");
        EXPECT_EQ(b.format_time(d), "3:46:00\u202fPM");
    }
    {
        BabelRequestContext ctx(app);
        b.get_babel(&app)->default_locale = "de_DE";
        EXPECT_EQ(b.format_datetime(d, "long"), "12. April 2010, 15:46:00 MESZ");
    }
}

TEST(TestDateFormatting, CustomFormats) {
    BabelApp app;
    app.config["BABEL_DEFAULT_LOCALE"] = "en_US";
    app.config["BABEL_DEFAULT_TIMEZONE"] = "Pacific/Johnston";
    Babel b(&app);
    b.date_formats["datetime"] = "long";
    b.date_formats["datetime.long"] = "MMMM d, yyyy h:mm:ss a";
    BabelDateTime d(2010, 4, 12, 13, 46);

    {
        BabelRequestContext ctx(app);
        EXPECT_EQ(b.format_datetime(d), "April 12, 2010 3:46:00 AM");
    }
}

TEST(TestDateFormatting, CustomLocaleSelector) {
    BabelApp app;
    Babel b(&app);
    BabelDateTime d(2010, 4, 12, 13, 46);

    std::string the_timezone = "UTC";
    std::string the_locale = "en_US";

    auto select_locale = [&the_locale]() { return the_locale; };
    auto select_timezone = [&the_timezone]() { return the_timezone; };

    b.get_babel(&app)->locale_selector = select_locale;
    b.get_babel(&app)->timezone_selector = select_timezone;

    {
        BabelRequestContext ctx(app);
        EXPECT_EQ(b.format_datetime(d), "Apr 12, 2010, 1:46:00\u202fPM");
    }
    the_locale = "de_DE";
    the_timezone = "Europe/Vienna";
    {
        BabelRequestContext ctx(app);
        EXPECT_EQ(b.format_datetime(d), "12.04.2010, 15:46:00");
    }
}

TEST(TestDateFormatting, Refreshing) {
    BabelApp app;
    Babel b(&app);
    BabelDateTime d(2010, 4, 12, 13, 46);
    {
        BabelRequestContext ctx(app);
        EXPECT_EQ(b.format_datetime(d), "Apr 12, 2010, 1:46:00\u202fPM");
        b.get_babel(&app)->default_timezone = "Europe/Vienna";
        b.refresh();
        EXPECT_EQ(b.format_datetime(d), "Apr 12, 2010, 3:46:00\u202fPM");
    }
}