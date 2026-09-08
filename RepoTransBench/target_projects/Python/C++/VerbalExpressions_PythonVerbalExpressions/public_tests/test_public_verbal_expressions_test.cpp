#include <gtest/gtest.h>
#include <string>
#include <regex>
#include "../include/verbal_expressions.h"

// Helper for checking a "fullmatch"
static bool is_fullmatch(const VerEx& verex, const std::string& str) {
    auto m = verex.match(str);
    return (!m.empty() && m[0] == str);
}

TEST(TestPublicVerbalExpressions, StartOfLine) {
    VerEx verex = VerEx().start_of_line().then("Begin");
    std::string s = "BeginAgain";
    std::string not_s = "NotBegin";
    ASSERT_TRUE(!verex.match(s).empty());
    ASSERT_TRUE(verex.match(not_s).empty());
}

TEST(TestPublicVerbalExpressions, Anything) {
    VerEx verex = VerEx().anything();
    ASSERT_TRUE(!verex.match("Some string").empty());
    ASSERT_TRUE(!verex.match("").empty());
}

TEST(TestPublicVerbalExpressions, AnythingBut) {
    VerEx verex = VerEx().anything_but("xyz");
    ASSERT_TRUE(!verex.match("Hello world").empty());
    auto m = verex.match("xyzworld");
    ASSERT_TRUE(!m.empty() && m[0] == "");
}

TEST(TestPublicVerbalExpressions, EndOfLine) {
    VerEx verex = VerEx().find("complete").end_of_line();
    auto m = verex.search("mission complete");
    ASSERT_TRUE(!m.empty());
    ASSERT_TRUE(verex.match("completely done").empty());
}

TEST(TestPublicVerbalExpressions, Maybe) {
    VerEx verex = VerEx().then("red").maybe("car");
    ASSERT_TRUE(is_fullmatch(verex, "red"));
    ASSERT_TRUE(is_fullmatch(verex, "redcar"));
    ASSERT_FALSE(is_fullmatch(verex, "redcars"));
}

TEST(TestPublicVerbalExpressions, AnyOf) {
    VerEx verex = VerEx().any("wxyz");
    ASSERT_TRUE(!verex.match("z").empty());
    ASSERT_TRUE(!verex.match("yell").empty());
    ASSERT_TRUE(verex.match("k").empty());
}

TEST(TestPublicVerbalExpressions, NotOf) {
    VerEx verex = VerEx().anything_but("LMN");
    ASSERT_TRUE(!verex.match("abcde").empty());
    auto m = verex.match("MMM");
    ASSERT_TRUE(!m.empty() && m[0] == "");
}

TEST(TestPublicVerbalExpressions, Replace) {
    VerEx verex = VerEx().find("swap_me");
    std::string text = "swap_me";
    std::string result = verex.replace("changed", text);
    ASSERT_EQ(result, "changed");
}