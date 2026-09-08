#include <gtest/gtest.h>
#include <string>
#include "babel_flask_babel/Babel.h"

TEST(TestNumberFormatting, Basics) {
    BabelApp app;
    Babel b(&app);
    int n = 1099;

    {
        BabelRequestContext ctx(app);
        EXPECT_EQ(b.format_number(n), "1,099");
        EXPECT_EQ(b.format_decimal("1010.99"), "1,010.99");
        EXPECT_EQ(b.format_currency(n, "USD"), "$1,099.00");
        EXPECT_EQ(b.format_percent(0.19), "19%");
        EXPECT_EQ(b.format_scientific(10000), "1E4");
    }
}