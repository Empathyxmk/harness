#include <gtest/gtest.h>
#include "fuzzywuzzy/process.h"

TEST(PublicProcessTest, ExtractOnePublic) {
    std::string query = "python programmer";
    std::vector<std::string> choices = {"java developer", "python engineer", "c++ guru"};
    auto [match, score] = fuzzywuzzy::process::extractOne(query, choices);
    EXPECT_TRUE(std::find(choices.begin(), choices.end(), match) != choices.end());
    EXPECT_TRUE(typeid(score) == typeid(int));
    EXPECT_GT(score, 0);
}
TEST(PublicProcessTest, ExtractBestsPublic) {
    std::string query = "data science";
    std::vector<std::string> choices = {"science data", "data analytics", "data scientist", "big data"};
    auto results = fuzzywuzzy::process::extractBests(query, choices, 2);
    EXPECT_EQ(results.size(), 2);
    for (const auto& [match, score] : results) {
        EXPECT_TRUE(std::find(choices.begin(), choices.end(), match) != choices.end());
        EXPECT_TRUE(typeid(score) == typeid(int));
        EXPECT_GT(score, 0);
    }
}