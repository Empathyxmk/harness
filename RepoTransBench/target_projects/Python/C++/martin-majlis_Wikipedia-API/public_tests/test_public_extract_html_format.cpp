#include <gtest/gtest.h>
#include "wikipedia_api_mock.h"

TEST(PublicExtractHtmlFormatTest, HtmlExtractHasHtmlElements) {
    Wikipedia wiki("public-html-format/1.0", "", "", ExtractFormat::HTML);
    auto page = wiki.page("Python (genus)");
    auto txt = page.text();
    ASSERT_TRUE(txt.find("<p>") != std::string::npos ||
                txt.find("<b>") != std::string::npos ||
                txt.find("<i>") != std::string::npos);
}

TEST(PublicExtractHtmlFormatTest, HtmlExtractTrimmedAndNonEmpty) {
    Wikipedia wiki("public-html-format/2.0", "", "", ExtractFormat::HTML);
    auto page = wiki.page("Computer");
    std::string txt = page.text();
    txt.erase(std::remove_if(txt.begin(), txt.end(), ::isspace), txt.end());
    ASSERT_GT(txt.size(), 0);
}