#include <gtest/gtest.h>
#include "fuzzywuzzy/process.h"
#include "fuzzywuzzy/fuzz.h"

TEST(ProcessTest, ExtractOne) {
    std::vector<std::string> choices = {"new york jets", "new york giants", "liverpool"};
    std::string query = "new york jets";
    auto res = fuzzywuzzy::process::extractOne(query, choices);
    EXPECT_TRUE(typeid(res) == typeid(std::pair<std::string,int>));
    EXPECT_EQ(res.first, "new york jets");
}

TEST(ProcessTest, ExtractLimitAndProcessor) {
    std::vector<std::string> choices = {"foo Xbar", "bar", "baz"};
    std::string query = "foo bar";
    auto res = fuzzywuzzy::process::extract(query, choices,
        [](const std::string& x){ return fuzzywuzzy::utils::to_lower(x); },
        fuzzywuzzy::fuzz::token_sort_ratio, 2
    );
    EXPECT_EQ(res.size(), 2);
}

TEST(ProcessTest, ExtractNone) {
    EXPECT_EQ(fuzzywuzzy::process::extractOne("", {}), std::pair<std::string,int>()); // or some std::optional type
    EXPECT_EQ(fuzzywuzzy::process::extract("", {}), std::vector<std::pair<std::string,int>>());
}

TEST(ProcessTest, EmptyChoicesExtractOne) {
    EXPECT_EQ(fuzzywuzzy::process::extractOne("a", {}), std::pair<std::string,int>());
    EXPECT_EQ(fuzzywuzzy::process::extract("a", {}), std::vector<std::pair<std::string,int>>());
}

TEST(ProcessTest, IndexedChoices) {
    std::map<std::string, std::string> choices = {{"a", "foo"}, {"b", "boo"}};
    auto out = fuzzywuzzy::process::extractOne("foo", choices);
    EXPECT_EQ(out.first, "foo");
}