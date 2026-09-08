#include <gtest/gtest.h>
#include "wikipedia_api_mock.h"

TEST(PublicBacklinksTest, BacklinksToArticle) {
    Wikipedia wiki("public-backlinks/1.0", "en");
    auto page = wiki.page("United States");
    auto backlinks = page.backlinks_list(); // Helper returns std::vector<WikipediaPagePtr>
    ASSERT_TRUE(typeid(backlinks) == typeid(std::vector<WikipediaPagePtr>));
    ASSERT_GT(backlinks.size(), 0);
}

TEST(PublicBacklinksTest, BacklinksGeneratorType) {
    Wikipedia wiki("public-backlinks/2.0", "en");
    auto page = wiki.page("Physics");
    auto backlinks_it = page.backlinks_gen();
    ASSERT_TRUE(typeid(*backlinks_it) == typeid(WikipediaPagePtr));
}