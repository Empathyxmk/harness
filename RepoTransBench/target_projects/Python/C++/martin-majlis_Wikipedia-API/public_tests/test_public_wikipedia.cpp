#include <gtest/gtest.h>
#include "wikipedia_api_mock.h"

TEST(PublicWikipediaTest, WikipediaLanguageSwitch) {
    Wikipedia wiki_en("public-wiki-test/1", "en");
    Wikipedia wiki_es("public-wiki-test/2", "es");
    auto page_en = wiki_en.page("Madrid");
    auto page_es = wiki_es.page("Madrid");
    ASSERT_TRUE(page_en.exists());
    ASSERT_TRUE(page_es.exists());
    ASSERT_EQ(wiki_en.language(), "en");
    ASSERT_EQ(wiki_es.language(), "es");
}

TEST(PublicWikipediaTest, WikipediaVariantUsage) {
    Wikipedia wiki("public-wiki-test/3", "zh", "zh-cn");
    auto page = wiki.page("北京");
    ASSERT_TRUE(page.exists());
    ASSERT_EQ(wiki.variant(), "zh-cn");
}