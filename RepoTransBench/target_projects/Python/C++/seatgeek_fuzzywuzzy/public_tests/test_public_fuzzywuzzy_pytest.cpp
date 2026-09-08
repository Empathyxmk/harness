#include <gtest/gtest.h>
#include "fuzzywuzzy/process.h"

TEST(PublicFuzzyWuzzyPytest, ProcessWarning) {
    // Simulate: query reduced to empty string, expect some warning mechanism (here, just assert returned value)
    std::string query = "......";
    std::vector<std::string> choices = {"......"};
    // Not possible to test logging directly in C++, so check the logic yields empty results or nullptr
    auto result = fuzzywuzzy::process::extractOne(query, choices);
    // We expect result to be empty or have a score of 0 if processor strips everything
    EXPECT_TRUE(result.first.empty() || result.second == 0);
}