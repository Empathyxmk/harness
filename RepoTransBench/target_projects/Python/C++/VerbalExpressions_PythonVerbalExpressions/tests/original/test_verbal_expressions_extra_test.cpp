#include <gtest/gtest.h>
#include <regex>
#include "../../include/verbal_expressions.h"

class VerExExtraTest : public ::testing::Test {
protected:
    void SetUp() override {
        v = new VerEx();
    }
    void TearDown() override {
        delete v;
        v = nullptr;
    }
    VerEx* v;
};

TEST_F(VerExExtraTest, Anything) {
    VerEx ver = VerEx().anything();
    auto re = ver.regex();
    ASSERT_TRUE(std::regex_search("abcdef", re));
}

TEST_F(VerExExtraTest, AnythingBut) {
    VerEx ver = VerEx().anything_but("x");
    auto re = ver.regex();
    ASSERT_TRUE(std::regex_search("abc", re));
    ASSERT_TRUE(std::regex_search("", re));
    std::smatch m;
    std::regex fullre(ver.source());
    ASSERT_FALSE(std::regex_match("x", fullre)); // fullmatch equivalent
    ASSERT_TRUE(std::regex_search("abcdef", re));
}

TEST_F(VerExExtraTest, EndOfLine) {
    VerEx ver = VerEx().end_of_line();
    std::regex re(ver.source() + "$");
    ASSERT_TRUE(std::regex_search("end$", re));
}

TEST_F(VerExExtraTest, Maybe) {
    VerEx ver = VerEx().maybe("abc");
    std::regex re = ver.regex();
    ASSERT_TRUE(std::regex_search("abc", re));
    ASSERT_TRUE(std::regex_search("", re));
}

TEST_F(VerExExtraTest, StartOfLine) {
    VerEx ver = VerEx().start_of_line();
    std::string pattern = ver.source();
    ASSERT_TRUE(pattern.rfind("^", 0) == 0);
}

TEST_F(VerExExtraTest, FindAndThen) {
    VerEx v1 = VerEx().find("cat");
    std::regex re1 = v1.regex();
    ASSERT_TRUE(std::regex_search("cat", re1));
    VerEx v2 = VerEx().then("dog");
    std::regex re2 = v2.regex();
    ASSERT_TRUE(std::regex_search("dog", re2));
}

TEST_F(VerExExtraTest, AnyAndAnyOf) {
    VerEx v = VerEx().any("abc");
    std::regex re = v.regex();
    ASSERT_TRUE(std::regex_search("a", re));
    ASSERT_TRUE(std::regex_search("b", re));
    ASSERT_FALSE(std::regex_match("d", re));
    VerEx v2 = VerEx().any_of("xyz");
    std::regex re2 = v2.regex();
    ASSERT_TRUE(std::regex_search("z", re2));
}

TEST_F(VerExExtraTest, LineBreakBr) {
    VerEx v = VerEx().line_break();
    std::regex re = v.regex();
    ASSERT_TRUE(std::regex_search("\n", re));
    ASSERT_TRUE(std::regex_search("\r\n", re));
    VerEx v2 = VerEx().br();
    std::regex re2 = v2.regex();
    ASSERT_TRUE(std::regex_search("\n", re2));
}

TEST_F(VerExExtraTest, RangeWithOddArgs) {
    VerEx v = VerEx().range({"a", "c", "0", "1"});
    std::regex re = v.regex();
    ASSERT_TRUE(std::regex_search("a", re));
    ASSERT_TRUE(std::regex_search("b", re));
    ASSERT_TRUE(std::regex_search("c", re));
    ASSERT_TRUE(std::regex_search("0", re));
    ASSERT_TRUE(std::regex_search("1", re));
}

TEST_F(VerExExtraTest, TabAndWord) {
    VerEx v = VerEx().tab();
    std::regex re = v.regex();
    ASSERT_TRUE(std::regex_search("\t", re));
    VerEx w = VerEx().word();
    std::regex re2 = w.regex();
    ASSERT_TRUE(std::regex_search("wordtest", re2));
}

TEST_F(VerExExtraTest, OrWithoutValue) {
    VerEx v = VerEx().find("foo").OR();
    std::string src = v.source();
    ASSERT_NE(src.find("|"), std::string::npos);
    // In C++, all member functions are accessible, so just test type-compatibility
}

TEST_F(VerExExtraTest, OrWithValue) {
    VerEx v = VerEx().find("foo").OR("bar");
    std::string src = v.source();
    ASSERT_NE(src.find("|(bar)"), std::string::npos);
}

TEST_F(VerExExtraTest, Replace) {
    VerEx v = VerEx().find("foo");
    std::string input = "foofoo";
    auto result = v.replace("bar", input);
    ASSERT_EQ(result, "barbar");
}

TEST_F(VerExExtraTest, WithAnyCase) {
    VerEx v = VerEx().find("abc").with_any_case(true);
    ASSERT_EQ(v.modifiers['I'], std::regex_constants::icase);
    v.with_any_case(false);
    ASSERT_EQ(v.modifiers['I'], 0);
}

TEST_F(VerExExtraTest, SearchOneLine) {
    VerEx v = VerEx().search_one_line(true);
    ASSERT_EQ(v.modifiers['M'], std::regex_constants::multiline);
    v.search_one_line(false);
    ASSERT_EQ(v.modifiers['M'], 0);
}

TEST_F(VerExExtraTest, WithAscii) {
    VerEx v = VerEx().with_ascii(true);
    ASSERT_EQ(v.modifiers['A'], std::regex_constants::ECMAScript);
    v.with_ascii(false);
    ASSERT_EQ(v.modifiers['A'], 0);
}

TEST_F(VerExExtraTest, ValueAndSource) {
    VerEx v = VerEx().find("cat");
    ASSERT_EQ(v.value(), v.source());
    ASSERT_EQ(v.raw(), v.source());
}