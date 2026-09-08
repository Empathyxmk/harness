#include <gtest/gtest.h>
#include "wikipedia_api_mock.h"

TEST(PublicLangLinksTest, LangLinksOnPage) {
    Wikipedia wiki("public-langlinks/1.0");
    auto page = wiki.page("Earth");
    auto langlinks = page.langlinks();
    ASSERT_TRUE(typeid(langlinks) == typeid(std::unordered_map<std::string, WikipediaPagePtr>));
    ASSERT_GE(langlinks.size(), 2);
    ASSERT_TRUE(langlinks.contains("es") || langlinks.contains("fr"));
}

TEST(PublicLangLinksTest, LangLinksEmptyOnNonexistent) {
    Wikipedia wiki("public-langlinks/2.0");
    auto page = wiki.page("QwertyuiopasdfghjklzxcvbnmNonExistent");
    ASSERT_TRUE(page.langlinks().empty());
}