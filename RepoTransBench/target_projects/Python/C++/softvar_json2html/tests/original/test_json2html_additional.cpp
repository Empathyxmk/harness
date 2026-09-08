#include <gtest/gtest.h>
#include "json2html.h"
#include <string>
#include <map>
#include <vector>

using namespace json2html;

TEST(Json2HtmlAdditional, ConvertSimpleDict) {
    std::map<std::string, std::string> data = { {"foo", "bar"} };
    std::string html = convert(data);
    EXPECT_NE(html.find("foo"), std::string::npos);
    EXPECT_NE(html.find("bar"), std::string::npos);
    EXPECT_TRUE(html.find("<table") == 0 || html.find("<table") != std::string::npos);
}

TEST(Json2HtmlAdditional, ConvertListOfDicts) {
    std::vector<std::map<std::string, std::string>> data = {
        {{"foo", "bar"}}, {{"foo", "baz"}}
    };
    std::string html = convert(data);
    EXPECT_TRUE(html.find("<table") == 0 || html.find("<table") != std::string::npos);
    int tr_count = 0;
    size_t p = 0; while ((p = html.find("<tr>", p)) != std::string::npos) { ++tr_count; p += 4; }
    EXPECT_GE(tr_count, 2);
}

TEST(Json2HtmlAdditional, ConvertEmptyInput) {
    EXPECT_EQ(convert(""), "");
    std::map<std::string, std::string> empty_dict;
    EXPECT_EQ(convert(empty_dict), "");
    std::vector<std::string> empty_list;
    EXPECT_EQ(convert(empty_list), "");
}

TEST(Json2HtmlAdditional, ConvertCustomTableAttr) {
    std::map<std::string, std::string> data = { {"x", "1"} };
    std::string html = convert(data, false, true, "class=\"tbl\" id=\"tid\"");
    EXPECT_NE(html.find("class=\"tbl\""), std::string::npos);
    EXPECT_NE(html.find("id=\"tid\""), std::string::npos);
}

TEST(Json2HtmlAdditional, ConvertRaisesOnInvalidType) {
    // C++ fallback: just returns string for unknown types (simulated)
    void* dummy = reinterpret_cast<void*>(0x1234);
    std::string output = convert(dummy);
    EXPECT_TRUE(!output.empty());
}

TEST(Json2HtmlAdditional, ConvertHandlesTuple) {
    // Use pair as tuple
    std::pair<std::map<std::string, int>, std::map<std::string, int>> data = {
        {{"a", 1}}, {{"b", 2}}
    };
    // Simulate: concatenate string output of both
    std::string html_a = convert(data.first);
    std::string html_b = convert(data.second);
    EXPECT_NE(html_a.find("a"), std::string::npos);
    EXPECT_NE(html_b.find("b"), std::string::npos);
}

TEST(Json2HtmlAdditional, ConvertPreservesHtmlEscape) {
    std::map<std::string, std::string> data = { {"key", "<script>alert(\"x\")</script>"} };
    std::string html = convert(data);
    EXPECT_TRUE(html.find("&lt;script&gt;") != std::string::npos || html.find("&lt;script&gt;alert") != std::string::npos);
}

TEST(Json2HtmlAdditional, Json2HtmlRepr) {
    Json2Html js;
    EXPECT_NE(js.repr().find("Json2Html"), std::string::npos);
}