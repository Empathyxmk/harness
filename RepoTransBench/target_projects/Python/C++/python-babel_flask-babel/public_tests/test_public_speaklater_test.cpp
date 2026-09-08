#include <gtest/gtest.h>
#include <string>
#include "babel_flask_babel/LazyString.h"

TEST(TestPublicSpeaklater, LazyStringStrAddition) {
    LazyString s([](){ return "alpha"; });
    EXPECT_EQ(s + std::string("beta"), "alphabeta");
    EXPECT_EQ(std::string("BETA:") + s, "BETA:alpha");
}

TEST(TestPublicSpeaklater, LazyStringRepeat) {
    LazyString s([](){ return "xy"; });
    EXPECT_EQ(s * 3, "xyxyxy");
    EXPECT_EQ(3 * s, "xyxyxy");
}

TEST(TestPublicSpeaklater, LazyStringFormatting) {
    LazyString s([](const std::string& name){ return "Hello, " + name + "!"; }, "Haruka");
    EXPECT_EQ((std::string)s, "Hello, Haruka!");
}

TEST(TestPublicSpeaklater, LazyStringHtml) {
    LazyString s([](){ return "<p>Test</p>"; });
    EXPECT_EQ(s.html(), "<p>Test</p>");
}

TEST(TestPublicSpeaklater, LazyStringComparisons) {
    LazyString s1([](){ return "ten"; });
    LazyString s2([](){ return "twenty"; });
    EXPECT_TRUE(s1 < s2);
    EXPECT_TRUE(s2 > s1);
    EXPECT_TRUE(s1 != s2);
    EXPECT_FALSE(s1 == s2);
}