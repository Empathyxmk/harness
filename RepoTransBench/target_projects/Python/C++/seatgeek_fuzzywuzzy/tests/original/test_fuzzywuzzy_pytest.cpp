#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <stdexcept>
#include "fuzzywuzzy/process.h"
#include "fuzzywuzzy/fuzz.h"

// Test that when a processor reduces a string to empty, the system reacts as expected.
// In C++, this should throw or return a score of 0, or log a warning.
// We'll test for score/result being 0 for such cases.

TEST(ProcessPytest, ProcessExtractOneEmptyString) {
    std::string query = ":::::::";
    std::vector<std::string> choices = {":::::::"};

    // Call extractOne with a processor function that reduces all to empty string.
    // Assuming fuzzywuzzy::process::extractOne returns a pair<string, int>.
    auto result = fuzzywuzzy::process::extractOne(query, choices, fuzzywuzzy::fuzz::ratio, 
        [](const std::string& s) {
            std::string out;
            for (char c : s) {
                if (isalnum(static_cast<unsigned char>(c)))
                    out += c;
            }
            return out;
        }
    );
    // Since both reduce to empty string, ratio is 0.
    EXPECT_EQ(result.second, 0);
}