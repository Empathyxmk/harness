#include <gtest/gtest.h>
#include <string>
#include "babel_flask_babel/LazyString.h"

std::string basic_func(int x, int y = 2) {
    return "value(" + std::to_string(x) + "," + std::to_string(y) + ")";
}

TEST(TestSpeaklater, StrAndRepr) {
    LazyString lz(basic_func, 1, 3);
    EXPECT_EQ((std::string)lz, "value(1,3)");
    EXPECT_EQ(lz.repr(), "l'value(1,3)'");
}

TEST(TestSpeaklater, LenGetitemIterContains) {
    LazyString lz([](){ return "hello world"; });
    EXPECT_EQ(lz.length(), 11);
    EXPECT_EQ(lz.get(0), 'h');
    EXPECT_EQ(lz.substr(1, 4), "ello");
    std::string joined;
    for (char c : lz) { joined.push_back(c); }
    EXPECT_EQ(joined, "hello world");
    EXPECT_TRUE(lz.contains("hello"));
    EXPECT_FALSE(lz.contains("xxx"));
}

TEST(TestSpeaklater, AddRadd) {
    LazyString lz([](){ return "foo"; });
    EXPECT_EQ(lz + std::string("bar"), "foobar");
    EXPECT_EQ(std::string("bar") + lz, "barfoo");
}

TEST(TestSpeaklater, MulRmul) {
    LazyString lz([](){ return "a"; });
    EXPECT_EQ(lz * 3, "aaa");
    EXPECT_EQ(3 * lz, "aaa");
}

TEST(TestSpeaklater, Comparisons) {
    LazyString lz([](){ return "b"; });
    EXPECT_TRUE(lz > "a");
    EXPECT_TRUE(lz >= "b");
    EXPECT_TRUE(lz < "d");
    EXPECT_TRUE(lz <= "b");
    EXPECT_TRUE(lz == "b");
    EXPECT_TRUE(lz != "a");
}

TEST(TestSpeaklater, HtmlHashMod) {
    LazyString lz([](){ return "foo 7"; });
    EXPECT_EQ(lz.html(), "foo 7");
    EXPECT_EQ((size_t)lz.hash(), std::hash<std::string>{}("foo 7"));
    EXPECT_EQ(lz.mod("s"), "foo 7");
    EXPECT_EQ("bar: " + (std::string)lz, "bar: foo 7");
}

TEST(TestSpeaklater, GetAttrPassthroughAndError) {
    LazyString lz([](){ return "abcdef"; });
    EXPECT_EQ(lz.upper(), "ABCDEF");
    EXPECT_THROW(lz.nonexistent(), std::runtime_error);
    EXPECT_THROW(lz.get_attr("__setstate__"), std::runtime_error);
}

TEST(TestSpeaklater, KwargsArePassed) {
    auto f = [](const std::string& x = "") { std::string s = x; for (auto &ch : s) ch = toupper(ch); return s; };
    LazyString lz(f, "abc");
    EXPECT_EQ((std::string)lz, "ABC");
}

TEST(TestSpeaklater, EdgeCaseStrConversion) {
    LazyString lz([](){ return std::to_string(123); });
    EXPECT_EQ((std::string)lz, "123");
}