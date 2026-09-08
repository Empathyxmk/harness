#include <gtest/gtest.h>
#include <regex>
#include <vector>
#include "../../include/verbal_expressions.h"

class VerExTest : public ::testing::Test {
protected:
    void SetUp() override {
        v = new VerEx();
    }
    void TearDown() override {
        delete v;
        v = nullptr;
        // exp is handled per-test
    }
    VerEx* v;
    VerEx* exp;
};

TEST_F(VerExTest, ShouldRenderVerExAsString) {
    ASSERT_EQ(std::string(VerEx().add("^$").source()), "^$");
}

TEST_F(VerExTest, ShouldRenderVerExListAsString) {
    std::vector<std::string> parts = {"^", "[0-9]", "$"};
    ASSERT_EQ(std::string(VerEx().add(parts).source()), "^[0-9]$");
}

TEST_F(VerExTest, ShouldMatchCharactersInRange) {
    VerEx exp = v->start_of_line().range({"a", "c"});
    auto re = exp.regex();
    std::vector<std::string> chars = {"a", "b", "c"};
    for (auto& c : chars) {
        ASSERT_TRUE(std::regex_search(c, re));
    }
}

TEST_F(VerExTest, ShouldNotMatchCharactersOutsideOfRange) {
    VerEx exp = v->start_of_line().range({"a", "c"});
    auto re = exp.regex();
    ASSERT_FALSE(std::regex_search("d", re));
}

TEST_F(VerExTest, ShouldMatchCharactersInExtendedRange) {
    VerEx exp = v->start_of_line().range({"a", "b", "X", "Z"});
    auto re = exp.regex();
    std::vector<std::string> chars1 = {"a", "b"};
    std::vector<std::string> chars2 = {"X", "Y", "Z"};
    for (auto& c : chars1) {
        ASSERT_TRUE(std::regex_search(c, re));
    }
    for (auto& c : chars2) {
        ASSERT_TRUE(std::regex_search(c, re));
    }
}

TEST_F(VerExTest, ShouldNotMatchCharactersOutsideOfExtendedRange) {
    VerEx exp = v->start_of_line().range({"a", "b", "X", "Z"});
    auto re = exp.regex();
    ASSERT_FALSE(std::regex_search("c", re));
    ASSERT_FALSE(std::regex_search("W", re));
}

TEST_F(VerExTest, ShouldMatchStartOfLine) {
    VerEx exp = v->start_of_line();
    auto re = exp.regex();
    ASSERT_TRUE(std::regex_search("text  ", re));
}

TEST_F(VerExTest, ShouldMatchEndOfLine) {
    VerEx exp = v->start_of_line().end_of_line();
    auto re = exp.regex();
    ASSERT_TRUE(std::regex_search("", re));
}

TEST_F(VerExTest, ShouldMatchAnything) {
    VerEx exp = v->start_of_line().anything().end_of_line();
    auto re = exp.regex();
    ASSERT_TRUE(std::regex_search("!@#$%¨&*()__+{}", re));
}

TEST_F(VerExTest, ShouldMatchAnythingButSpecifiedWhenElementIsNotFound) {
    VerEx exp = v->start_of_line().anything_but("X").end_of_line();
    auto re = exp.regex();
    ASSERT_TRUE(std::regex_search("Y Files", re));
}

TEST_F(VerExTest, ShouldNotMatchAnythingButSpecifiedWhenElementIsFound) {
    VerEx exp = v->start_of_line().anything_but("X").end_of_line();
    auto re = exp.regex();
    ASSERT_FALSE(std::regex_search("VerEX", re));
}

TEST_F(VerExTest, ShouldFindElement) {
    VerEx exp = v->start_of_line().find("Wally").end_of_line();
    auto re = exp.regex();
    ASSERT_TRUE(std::regex_search("Wally", re));
}

TEST_F(VerExTest, ShouldNotFindMissingElement) {
    VerEx exp = v->start_of_line().find("Wally").end_of_line();
    auto re = exp.regex();
    ASSERT_FALSE(std::regex_search("Wall-e", re));
}

TEST_F(VerExTest, ShouldMatchWhenMaybeElementIsPresent) {
    VerEx exp = v->start_of_line().find("Python2.").maybe("7").end_of_line();
    auto re = exp.regex();
    ASSERT_TRUE(std::regex_search("Python2.7", re));
}

TEST_F(VerExTest, ShouldMatchWhenMaybeElementIsMissing) {
    VerEx exp = v->start_of_line().find("Python2.").maybe("7").end_of_line();
    auto re = exp.regex();
    ASSERT_TRUE(std::regex_search("Python2.", re));
}

TEST_F(VerExTest, ShouldMatchOnAnyWhenElementIsFound) {
    VerEx exp = v->start_of_line().any("Q").anything().end_of_line();
    auto re = exp.regex();
    ASSERT_TRUE(std::regex_search("Query", re));
}

TEST_F(VerExTest, ShouldNotMatchOnAnyWhenElementNotFound) {
    VerEx exp = v->start_of_line().any("Q").anything().end_of_line();
    auto re = exp.regex();
    ASSERT_FALSE(std::regex_search("W", re));
}

TEST_F(VerExTest, ShouldMatchWhenLineBreakPresent) {
    VerEx exp = v->start_of_line().anything().line_break().anything().end_of_line();
    auto re = exp.regex();
    ASSERT_TRUE(std::regex_search("Marco \n Polo", re));
}

TEST_F(VerExTest, ShouldMatchWhenLineBreakAndCRPresent) {
    VerEx exp = v->start_of_line().anything().line_break().anything().end_of_line();
    auto re = exp.regex();
    ASSERT_TRUE(std::regex_search("Marco \r\n Polo", re));
}

TEST_F(VerExTest, ShouldNotMatchWhenLineBreakIsMissing) {
    VerEx exp = v->start_of_line().anything().line_break().anything().end_of_line();
    auto re = exp.regex();
    ASSERT_FALSE(std::regex_search("Marco Polo", re));
}

TEST_F(VerExTest, ShouldMatchWhenTabPresent) {
    VerEx exp = v->start_of_line().anything().tab().end_of_line();
    auto re = exp.regex();
    ASSERT_TRUE(std::regex_search("One tab only\t", re));
}

TEST_F(VerExTest, ShouldNotMatchWhenTabIsMissing) {
    VerEx exp = v->start_of_line().anything().tab().end_of_line();
    auto re = exp.regex();
    ASSERT_FALSE(std::regex_search("No tab here", re));
}

TEST_F(VerExTest, ShouldMatchWhenWordPresent) {
    VerEx exp = v->start_of_line().anything().word().end_of_line();
    auto re = exp.regex();
    ASSERT_TRUE(std::regex_search("Oneword", re));
}

TEST_F(VerExTest, ShouldNotMatchWhenTwoWordsInsteadOfOne) {
    VerEx exp = v->start_of_line().anything().tab().end_of_line();
    auto re = exp.regex();
    ASSERT_FALSE(std::regex_search("Two words", re));
}

TEST_F(VerExTest, ShouldMatchWhenOrConditionFulfilled) {
    VerEx exp = v->start_of_line().anything().find("G").OR().find("h").end_of_line();
    auto re = exp.regex();
    ASSERT_TRUE(std::regex_search("Github", re));
}

TEST_F(VerExTest, ShouldNotMatchWhenOrConditionNotFulfilled) {
    VerEx exp = v->start_of_line().anything().find("G").OR().find("h").end_of_line();
    auto re = exp.regex();
    ASSERT_FALSE(std::regex_search("Bitbucket", re));
}

TEST_F(VerExTest, ShouldMatchOnUpperCaseWhenLowerAndAnyCaseTrue) {
    VerEx exp = v->start_of_line().find("THOR").end_of_line().with_any_case(true);
    auto re = exp.regex();
    ASSERT_TRUE(std::regex_search("thor", re));
}

TEST_F(VerExTest, ShouldMatchMultipleLines) {
    VerEx exp = v->start_of_line().anything().find("Pong").anything().end_of_line().search_one_line(true);
    auto re = exp.regex();
    ASSERT_TRUE(std::regex_search("Ping \n Pong \n Ping", re));
}

TEST_F(VerExTest, ShouldMatchEmailAddress) {
    VerEx exp = v->start_of_line().word().then("@").word().then(".").word().end_of_line();
    auto re = exp.regex();
    ASSERT_TRUE(std::regex_search("mail@mail.com", re));
}

TEST_F(VerExTest, ShouldMatchUrl) {
    VerEx exp = v->start_of_line().then("http").maybe("s").then("://").maybe("www.").word().then(".").word().maybe("/").end_of_line();
    auto re = exp.regex();
    ASSERT_TRUE(std::regex_search("https://www.google.com/", re));
}