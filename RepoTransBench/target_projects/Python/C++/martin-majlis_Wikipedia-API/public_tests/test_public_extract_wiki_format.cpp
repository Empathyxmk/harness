#include <gtest/gtest.h>
#include "wikipedia_api_mock.h"

TEST(PublicExtractWikiFormatTest, ExtractWikiContainsSection) {
    Wikipedia wiki("public-wiki-format/1.0", "", "", ExtractFormat::WIKI);
    auto page = wiki.page("Computer science");
    auto txt = page.text();
    ASSERT_TRUE(txt.find("== History ==") != std::string::npos ||
                txt.find("== history ==") != std::string::npos);
}

TEST(PublicExtractWikiFormatTest, ExtractWikiNotEmpty) {
    Wikipedia wiki("public-wiki-format/2.0", "", "", ExtractFormat::WIKI);
    auto page = wiki.page("Mathematics");
    ASSERT_GT(page.text().size(), 0);
}