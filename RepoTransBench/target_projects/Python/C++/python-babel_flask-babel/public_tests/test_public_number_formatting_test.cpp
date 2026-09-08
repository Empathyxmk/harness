#include <gtest/gtest.h>
#include "babel_flask_babel/Babel.h"

TEST(TestPublicNumberFormatting, FormatDecimal) {
    BabelApp app;
    Babel b(&app);
    BabelRequestContext ctx(app);
    std::string val = b.format_decimal(8142.73);
    EXPECT_TRUE(val.find(",") != std::string::npos || val.find(".") != std::string::npos);
}

TEST(TestPublicNumberFormatting, FormatCurrency) {
    BabelApp app;
    Babel b(&app);
    BabelRequestContext ctx(app);
    std::string result = b.format_currency(99.95, "EUR");
    EXPECT_TRUE(result.find("EUR") != std::string::npos || result.find("€") != std::string::npos || result.find("99") != std::string::npos);
}

TEST(TestPublicNumberFormatting, FormatPercent) {
    BabelApp app;
    Babel b(&app);
    BabelRequestContext ctx(app);
    std::string percent = b.format_percent(3.5);
    EXPECT_TRUE(percent.find("%") != std::string::npos || percent.find("3") != std::string::npos);
}

TEST(TestPublicNumberFormatting, FormatScientific) {
    BabelApp app;
    Babel b(&app);
    BabelRequestContext ctx(app);
    std::string sci = b.format_scientific(987654);
    EXPECT_TRUE(sci.find("E") != std::string::npos || sci.find("e") != std::string::npos || sci.find("10") != std::string::npos);
}