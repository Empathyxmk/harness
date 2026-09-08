#include <gtest/gtest.h>
#include "wikipedia_api_mock.h"

TEST(PublicLinksTest, PublicLinksExistInArticle) {
    Wikipedia wiki("public_link/1.0");
    auto page = wiki.page("Python (mythology)");
    auto links = page.links();
    ASSERT_TRUE(links.contains("Delphi") || links.contains("Apollo"));
}

TEST(PublicLinksTest, PublicLinksAreDictType) {
    Wikipedia wiki("public_link/2.0");
    auto page = wiki.page("Monty Python");
    auto& links = page.links();
    for (const auto& kv : links) {
        ASSERT_TRUE(typeid(kv.first) == typeid(std::string));
        ASSERT_TRUE(typeid(kv.second) == typeid(WikipediaPagePtr));
    }
}