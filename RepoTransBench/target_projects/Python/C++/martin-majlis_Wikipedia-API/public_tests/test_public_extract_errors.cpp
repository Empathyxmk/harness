#include <gtest/gtest.h>
#include "wikipedia_api_mock.h"

TEST(PublicExtractErrorsTest, InvalidPageReturnsFalse) {
    Wikipedia wiki("public-extract-error/1.0");
    auto page = wiki.page("CompletelyNonExistentArticleTotally");
    ASSERT_FALSE(page.exists());
    ASSERT_EQ(page.title(), "CompletelyNonExistentArticleTotally");
    ASSERT_EQ(page.text(), "");
}

TEST(PublicExtractErrorsTest, NonexistentCategoryReturnsFalse) {
    Wikipedia wiki("public-extract-error/2.0");
    auto cat = wiki.page("Category:TotallyFakeCategoryNeverExists");
    ASSERT_FALSE(cat.exists());
    ASSERT_EQ(cat.title(), "Category:TotallyFakeCategoryNeverExists");
    ASSERT_EQ(cat.summary(), "");
}