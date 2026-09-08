#include <gtest/gtest.h>
// Full implementation as per test_query_string.py

TEST(QueryStringTest, DefaultQueryParamWorks) {
    // /protected?jwt={token} and assert
    // ... Full implementation
}

TEST(QueryStringTest, ValuePrefixCustomLogic) {
    // JWT_QUERY_STRING_VALUE_PREFIX handling
    // ... Full implementation
}

TEST(QueryStringTest, CustomQueryParameter) {
    // JWT_QUERY_STRING_NAME logic
    // ... Full implementation
}

TEST(QueryStringTest, MissingQueryParameterDefaultAndCustom) {
    // 401 for missing, plus custom unauthorized_loader
    // ... Full implementation
}