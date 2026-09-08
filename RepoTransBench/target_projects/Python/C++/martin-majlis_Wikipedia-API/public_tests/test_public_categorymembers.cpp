#include <gtest/gtest.h>
#include "wikipedia_api_mock.h"

TEST(PublicCategoryMembersTest, CategoryMembersCategory) {
    Wikipedia wiki("public-catmembers/1.0");
    auto cat = wiki.page("Category:Mathematics");
    auto members = cat.categorymembers();
    std::vector<std::string> titles;
    for (const auto& kv : members) titles.push_back(kv.first);
    ASSERT_TRUE(std::any_of(
        titles.begin(), titles.end(),
        [](const std::string& t) { return !t.empty() && (t[0]=='A' || t[0]=='G'); }
    ));
}

TEST(PublicCategoryMembersTest, CategoryMembersAreDict) {
    Wikipedia wiki("public-catmembers/2.0");
    auto cat = wiki.page("Category:Science");
    ASSERT_TRUE(typeid(cat.categorymembers()) == typeid(std::unordered_map<std::string, WikipediaPagePtr>));
}