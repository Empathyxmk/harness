#include <gtest/gtest.h>
#include "wikipedia_api_mock.h"

TEST(PublicCategoriesTest, PublicCategoriesExist) {
    Wikipedia wiki("public-categories/1.0");
    auto page = wiki.page("London");
    auto categories = page.categories();
    ASSERT_TRUE(typeid(categories) == typeid(std::unordered_map<std::string, WikipediaPagePtr>));
    ASSERT_TRUE(std::any_of(
        categories.begin(), categories.end(),
        [](const auto& entry) {
            return entry.first.find("England") != std::string::npos ||
                   entry.first.find("Cities") != std::string::npos;
        }
    ));
}

TEST(PublicCategoriesTest, PublicCategoriesEmptyOnInvalidPage) {
    Wikipedia wiki("public-categories/2.0");
    auto page = wiki.page("PageThatDoesNotExistRandom42");
    ASSERT_TRUE(page.categories().empty());
}