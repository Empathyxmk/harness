#include <gtest/gtest.h>
#include "json2html.h"
#include <string>
#include <map>
#include <vector>

using namespace json2html;

TEST(PublicAdditional, Json2HtmlInstanceConversion) {
    Json2Html j2h;
    std::map<std::string, std::string> data = { {"fruit", "banana"}, {"quantity", "12"} };
    std::string html = j2h.convert(data);
    EXPECT_NE(html.find("banana"), std::string::npos);
    EXPECT_NE(html.find("quantity"), std::string::npos);
}

TEST(PublicAdditional, Json2HtmlFunctionConversion) {
    std::map<std::string, std::string> data = { {"planet", "Mars"}, {"distance", "225"} };
    std::string html = convert(data);
    EXPECT_NE(html.find("Mars"), std::string::npos);
    EXPECT_NE(html.find("distance"), std::string::npos);
}

TEST(PublicAdditional, ConvertDictWithNone) {
    std::map<std::string, std::string> data = { {"exists", "None"}, {"name", "test"} };
    std::string html = convert(data);
    EXPECT_TRUE(html.find("None") != std::string::npos || html.find("none") != std::string::npos);
}

TEST(PublicAdditional, ConvertBoolValues) {
    std::map<std::string, bool> data = { {"sunny", true}, {"rainy", false} };
    // We'll convert manually because our API expects string-valued map
    std::map<std::string, std::string> sdata;
    sdata["sunny"] = "True";
    sdata["rainy"] = "False";
    std::string html = convert(sdata);
    EXPECT_NE(html.find("True"), std::string::npos);
    EXPECT_NE(html.find("False"), std::string::npos);
}

TEST(PublicAdditional, ConvertListWithDictsAndStrings) {
    // Manually flatten for C++ test (simulate)
    std::vector<std::map<std::string, std::string>> dicts = {
        { {"animal", "dog"} },
        { {"animal", "bird"} }
    };
    std::string html1 = convert(dicts);
    EXPECT_NE(html1.find("dog"), std::string::npos);
    EXPECT_NE(html1.find("bird"), std::string::npos);
    // cat is a string element
    std::string html2 = convert("cat");
    EXPECT_NE(html2.find("cat"), std::string::npos);
}

TEST(PublicAdditional, Json2HtmlCustomTableAttributes) {
    std::map<std::string, std::string> data = { {"val", "40"} };
    std::string html = convert(data, false, true, "id=\"public_test_table\" class=\"newtab\"");
    EXPECT_NE(html.find("id=\"public_test_table\""), std::string::npos);
    EXPECT_NE(html.find("class=\"newtab\""), std::string::npos);
}

TEST(PublicAdditional, Json2HtmlListOfDictsDiff) {
    std::vector<std::map<std::string, std::string>> data = {
        { {"model", "A"}, {"year", "1990"} },
        { {"model", "B"}, {"year", "2020"} }
    };
    std::string html = convert(data);
    EXPECT_NE(html.find("model"), std::string::npos);
    EXPECT_NE(html.find("A"), std::string::npos);
    EXPECT_NE(html.find("B"), std::string::npos);
    EXPECT_NE(html.find("1990"), std::string::npos);
    EXPECT_NE(html.find("2020"), std::string::npos);
}

TEST(PublicAdditional, Json2HtmlEscapeScript) {
    std::map<std::string, std::string> data = { {"x", "<script>alert('a')</script>"} };
    std::string html = convert(data);
    EXPECT_NE(html.find("&lt;script&gt;"), std::string::npos);
    EXPECT_NE(html.find("alert"), std::string::npos);
}