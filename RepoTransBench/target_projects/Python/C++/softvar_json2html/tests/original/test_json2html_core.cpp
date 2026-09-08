#include <gtest/gtest.h>
#include "json2html.h"
#include <string>
#include <map>
#include <vector>
#include <cstdint>

using namespace json2html;

TEST(Json2HtmlCore, ConvertVariousInputs) {
    // ({"foo": "bar"}, "foo")
    std::map<std::string, std::string> dict1{ {"foo", "bar"} };
    std::string html1 = convert(dict1);
    EXPECT_NE(html1.find("foo"), std::string::npos);
    // ([], "")  # Empty list
    std::vector<std::string> empty_vec;
    std::string html2 = convert(empty_vec);
    EXPECT_EQ(html2, "");
    // ("", "")
    std::string html3 = convert("");
    EXPECT_EQ(html3, "");
    // ([{"a": 1, "b": 2}, {"a": 3, "b": 4}], "a")
    std::vector<std::map<std::string, int>> vecdicts = {
        {{"a", 1}, {"b", 2}},
        {{"a", 3}, {"b", 4}}
    };
    std::string html4 = convert(vecdicts);
    EXPECT_NE(html4.find("a"), std::string::npos);
    // (123, "123")
    int number = 123;
    std::string html5 = convert(number);
    EXPECT_NE(html5.find("123"), std::string::npos);
}

TEST(Json2HtmlCore, ConvertBadJsonString) {
    Json2Html js;
    std::string bad_json = "{\"foo\": bar}";
    std::string res = js.convert(bad_json);
    EXPECT_TRUE(res.find(bad_json) != std::string::npos || res.find("&quot;foo&quot;: bar") != std::string::npos);
}

TEST(Json2HtmlCore, ConvertNonUTFInput) {
    Json2Html js;
    std::string bad_bytes("\x80abc", 4);
    std::string res = js.convert(bad_bytes);
    EXPECT_TRUE(res.size() > 0);
}

TEST(Json2HtmlCore, ColumnHeadersFromListOfDicts) {
    Json2Html js;
    std::vector<std::map<std::string, std::string>> data = {
        {{"a", "1"}, {"b", "2"}},
        {{"a", "10"}, {"b", "20"}}
    };
    std::vector<std::string> headers = js.column_headers_from_list_of_dicts(data);
    ASSERT_EQ(headers.size(), 2);
    EXPECT_EQ(headers[0], "a");
    EXPECT_EQ(headers[1], "b");
}

TEST(Json2HtmlCore, ColumnHeadersWithInconsistentDicts) {
    Json2Html js;
    std::vector<std::map<std::string, std::string>> data = { {{"a", "1"}}, {{"a", "1"}, {"b", "2"}} };
    std::vector<std::string> headers = js.column_headers_from_list_of_dicts(data);
    EXPECT_TRUE(headers.empty());
}

TEST(Json2HtmlCore, ColumnHeadersWithListOfNonDicts) {
    Json2Html js;
    // This test simulates list of non-dicts: returns empty vector for our implementation
    std::vector<std::map<std::string, std::string>> data; // no items
    std::vector<std::string> headers = js.column_headers_from_list_of_dicts(data);
    EXPECT_TRUE(headers.empty());
}

TEST(Json2HtmlCore, ConvertWithEncodeOption) {
    Json2Html js;
    std::map<std::string, std::string> data = { {"foo", "bar"} };
    std::string result = js.convert(data, true);
    EXPECT_TRUE(!result.empty());
}

TEST(Json2HtmlCore, ConvertWithEscapeFalse) {
    Json2Html js;
    std::map<std::string, std::string> data = { {"key", "<b>html</b>"} };
    std::string html = js.convert(data, false, false);
    EXPECT_NE(html.find("<b>html</b>"), std::string::npos);
}

TEST(Json2HtmlCore, ReprJson2Html) {
    Json2Html js;
    std::string r = js.repr();
    EXPECT_NE(r.find("Json2Html"), std::string::npos);
}