#include <gtest/gtest.h>
#include <string>
#include "../include/verbal_expressions.h"

TEST(TestPublicVerbalExpressionsExtra, ReEscapePublic) {
    // C++ "re_escape" performs real escapes; here we test our implementation by round-trip property.
    ASSERT_EQ(re_escape("bar(foo)"), "bar\\(foo\\)");
    ASSERT_EQ(re_escape("hello?world."), "hello\\?world\\.");
    ASSERT_EQ(re_escape("[]{}"), "\\[\\]\\{\\}");
    ASSERT_EQ(re_escape("+*|"), "\\+\\*\\|");
}

TEST(TestPublicVerbalExpressionsExtra, VerexComplexPattern) {
    VerEx verex = VerEx().start_of_line().then("ftp://").maybe("downloads.").anything_but(" ").end_of_line();
    ASSERT_TRUE(!verex.match("ftp://files.com").empty());
    ASSERT_TRUE(!verex.match("ftp://downloads.files.com").empty());
    ASSERT_TRUE(verex.match("ftp:// downloads.files.com").empty());
}

TEST(TestPublicVerbalExpressionsExtra, VerexAnythingBut) {
    VerEx verex = VerEx().start_of_line().anything_but("xyz").end_of_line();
    ASSERT_TRUE(!verex.match("abc").empty());
    ASSERT_TRUE(verex.match("x").empty());
    ASSERT_TRUE(verex.match("y").empty());
    ASSERT_TRUE(!verex.match("").empty());
}

TEST(TestPublicVerbalExpressionsExtra, VerexRangePublic) {
    VerEx verex = VerEx().range({"a", "c"});
    auto pattern = verex.regex();
    ASSERT_TRUE(std::regex_search("xyzabc", pattern));
    ASSERT_TRUE(std::regex_search("b", pattern));
    ASSERT_FALSE(std::regex_search("g", pattern));
}

TEST(TestPublicVerbalExpressionsExtra, VerexMultipleOperators) {
    VerEx verex = VerEx().then("baz").maybe("qux").anything().end_of_line();
    ASSERT_TRUE(!verex.match("bazquxx").empty());
    ASSERT_TRUE(!verex.match("bazplus").empty());
    ASSERT_TRUE(!verex.match("baz").empty());
}

TEST(TestPublicVerbalExpressionsExtra, VerexAnyPublic) {
    VerEx verex = VerEx().any("QRST");
    ASSERT_TRUE(!verex.match("S").empty());
    ASSERT_TRUE(!verex.match("QRST").empty());
    ASSERT_TRUE(verex.match("P").empty());
}

TEST(TestPublicVerbalExpressionsExtra, VerexMatchPublic) {
    VerEx verex = VerEx().start_of_line().then("run").maybe("ner").end_of_line();
    auto m = verex.match("runner");
    ASSERT_FALSE(m.empty());
    ASSERT_EQ(m[0], "runner");
    auto m2 = verex.match("run");
    ASSERT_FALSE(m2.empty());
}

TEST(TestPublicVerbalExpressionsExtra, VerexReplacePublic) {
    VerEx verex = VerEx().find("error");
    std::string text = "error";
    std::string replaced = verex.replace("fixed", text);
    ASSERT_EQ(replaced, "fixed");
}