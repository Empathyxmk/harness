#include <gtest/gtest.h>
#include "json2html.h"
#include <string>
#include <map>
#include <vector>

using namespace json2html;

TEST(PublicCore, ConvertSimpleDict) {
    std::map<std::string, std::string> data = {{"animal", "Elephant"}, {"region", "Africa"}};
    std::string html = convert(data);
    EXPECT_NE(html.find("<th>animal</th>"), std::string::npos);
    EXPECT_NE(html.find("<td>Elephant</td>"), std::string::npos);
    EXPECT_NE(html.find("<th>region</th>"), std::string::npos);
    EXPECT_NE(html.find("<td>Africa</td>"), std::string::npos);
}

TEST(PublicCore, ConvertListOfNumbers) {
    std::vector<int> data = {400, 500, 600};
    std::string html = convert(data);
    EXPECT_EQ(html.find("<ul>"), 0);
    EXPECT_NE(html.find("<li>400</li>"), std::string::npos);
    EXPECT_NE(html.find("<li>500</li>"), std::string::npos);
    EXPECT_NE(html.find("<li>600</li>"), std::string::npos);
}

TEST(PublicCore, ConvertNestedDictList) {
    std::map<std::string, std::vector<std::map<std::string, std::string>>> data = {
        {"cars", { {{"make", "Toyota"}, {"year", "2010"}}, {{"make", "Ford"}, {"year", "2015"}} } }
    };
    // Flattened: just convert inside manually (simulate)
    std::string html = convert(data["cars"]);
    EXPECT_NE(html.find("Toyota"), std::string::npos);
    EXPECT_NE(html.find("Ford"), std::string::npos);
    EXPECT_TRUE(html.find("year") != std::string::npos && html.find("make") != std::string::npos);
}

TEST(PublicCore, ConvertJsonString) {
    std::string json_str = "{\"genre\": \"Jazz\", \"artist\": \"Miles Davis\"}";
    std::string html = convert(json_str);
    EXPECT_NE(html.find("<th>genre</th>"), std::string::npos);
    EXPECT_NE(html.find("<td>Jazz</td>"), std::string::npos);
    EXPECT_NE(html.find("Miles Davis"), std::string::npos);
}

TEST(PublicCore, ConvertEscapeHtml) {
    std::map<std::string, std::string> data = { {"malicious", "<img src='evil'>"} };
    std::string html = convert(data);
    EXPECT_NE(html.find("&lt;img"), std::string::npos);
}

TEST(PublicCore, ConvertBadJsonString) {
    std::string bad_json = "{\"foo\": bar";
    std::string html = convert(bad_json);
    EXPECT_TRUE(html.length() > 0);
    EXPECT_NE(html.find("{&quot;foo&quot;: bar"), std::string::npos);
}

TEST(PublicCore, ConvertEmptyObject) {
    std::map<std::string, std::string> data;
    std::string html = convert(data);
    EXPECT_EQ(html, "");
}

TEST(PublicCore, ConvertEmptyList) {
    std::vector<std::string> data;
    std::string html = convert(data);
    EXPECT_EQ(html, "");
}