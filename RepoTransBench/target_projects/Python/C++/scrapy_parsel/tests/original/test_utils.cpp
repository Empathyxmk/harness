#include <gtest/gtest.h>
#include "utils.h"
#include <stdexcept>

// Test shorten
TEST(UtilsTest, ShortenWidthCase) {
    EXPECT_THROW(shorten("foobar", -1), std::invalid_argument);
    EXPECT_EQ(shorten("foobar", 0), "");
    EXPECT_EQ(shorten("foobar", 1), ".");
    EXPECT_EQ(shorten("foobar", 2), "..");
    EXPECT_EQ(shorten("foobar", 3), "...");
    EXPECT_EQ(shorten("foobar", 4), "f...");
    EXPECT_EQ(shorten("foobar", 5), "fo...");
    EXPECT_EQ(shorten("foobar", 6), "foobar");
    EXPECT_EQ(shorten("foobar", 7), "foobar");
}

TEST(UtilsTest, ExtractRegexCases) {
    EXPECT_EQ(extract_regex(R"((\w+)\s*(\d+)\s*\,?\s*(\d+))", "October  25, 2019", true)[0], "October  25, 2019");
    EXPECT_EQ(extract_regex(R"((\w+)\s*(\d+)\s*\,?\s*(\d+))", "October  25 2019", true)[0], "October  25 2019");
    EXPECT_EQ(extract_regex(R"((\w+)\s*(\d+)\s*\,?\s*(\d+))", "October  25 2019", true)[0], "October  25 2019");
    EXPECT_EQ(extract_regex(R"(\w+\s*\d+\s*\,?\s*\d+)", "October  25 2019", true)[0], "October  25 2019");
    EXPECT_EQ(extract_regex(R"(^.*$)", R"(&quot;sometext&quot; &amp; &quot;moretext&quot;)", true)[0], R"(&quot;sometext&quot; &amp; &quot;moretext&quot;)");
    EXPECT_EQ(extract_regex(R"(^.*$)", R"(&quot;sometext&quot; &amp; &quot;moretext&quot;)", false)[0], R"(&quot;sometext&quot; &amp; &quot;moretext&quot;)");
}