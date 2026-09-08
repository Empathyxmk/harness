#include <gtest/gtest.h>
#include <string>
#include "babel_flask_babel/Babel.h"

TEST(TestPublicDateFormatting, FormatTime) {
    BabelApp app;
    Babel b(&app);
    BabelDateTime dt(2021, 8, 14, 22, 15, 30);

    BabelRequestContext ctx(app);
    std::string s = b.format_time(dt, "short");
    bool has_digit = false;
    for (char c : s) if (isdigit(c)) { has_digit = true; break; }
    EXPECT_TRUE(has_digit);
}

TEST(TestPublicDateFormatting, FormatDate) {
    BabelApp app;
    Babel b(&app);
    BabelDateTime d(2022, 7, 20);

    BabelRequestContext ctx(app);
    std::string s = b.format_date(d, "long");
    EXPECT_TRUE(s.find("2022") != std::string::npos || s.find("20") != std::string::npos);
}

TEST(TestPublicDateFormatting, FormatDateTime) {
    BabelApp app;
    Babel b(&app);
    BabelDateTime d(2020, 12, 31, 19, 45, 16);

    BabelRequestContext ctx(app);
    std::string s = b.format_datetime(d, "full");
    EXPECT_TRUE((s.find("2020") != std::string::npos || s.find("31") != std::string::npos) && s.find(":") != std::string::npos);
}

TEST(TestPublicDateFormatting, FormatTimedelta) {
    BabelApp app;
    Babel b(&app);
    BabelTimeDelta delta = BabelTimeDelta::days(3) + BabelTimeDelta::hours(1) + BabelTimeDelta::minutes(25);

    BabelRequestContext ctx(app);
    std::string s = b.format_timedelta(delta);
    EXPECT_TRUE(s.find("3") != std::string::npos || s.find("day") != std::string::npos);
}

TEST(TestPublicDateFormatting, FormatTimeCustomLocale) {
    BabelApp app;
    Babel b(&app);
    BabelDateTime dt(2023, 6, 15, 17, 40, 0);

    BabelRequestContext ctx(app);
    std::string s = b.format_time(dt, "short", "it");
    EXPECT_TRUE(s.find(":") != std::string::npos);
}