#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <algorithm>
#include <locale>
#include <codecvt>
#include "fuzzywuzzy/fuzz.h"
#include "fuzzywuzzy/utils.h"
#include "fuzzywuzzy/process.h"

// Helper function to convert wide string to UTF-8
std::string wstring_to_utf8(const std::wstring& str) {
    std::wstring_convert<std::codecvt_utf8<wchar_t>> conv;
    return conv.to_bytes(str);
}

class StringProcessingTest : public ::testing::Test {};

TEST_F(StringProcessingTest, ReplaceNonLettersNonNumbersWithWhitespace) {
    std::vector<std::string> inputs = {
        "new york mets - atlanta braves",
        "Cães danados",
        "New York //// Mets $$$",
        "Ça va?"
    };
    std::vector<std::string> wanted = {
        "new york mets   atlanta braves",
        "Cães danados",
        "New York     Mets    ",
        "Ça va "
    };

    for (size_t i = 0; i < inputs.size(); ++i) {
        ASSERT_EQ(fuzzywuzzy::utils::replace_non_letters_non_numbers_with_whitespace(inputs[i]), wanted[i]);
    }
}

class FuzzTest : public ::testing::Test {};

TEST_F(FuzzTest, RatioBasic) {
    EXPECT_EQ(fuzzywuzzy::fuzz::ratio("this is a test", "this is a test"), 100);
    EXPECT_EQ(fuzzywuzzy::fuzz::ratio("fuzzy wuzzy was a bear", "wuzzy fuzzy was a bear"), 90);
}

TEST_F(FuzzTest, PartialRatio) {
    EXPECT_EQ(fuzzywuzzy::fuzz::partial_ratio("test", "testa"), 100);
    EXPECT_EQ(fuzzywuzzy::fuzz::partial_ratio("test", "tesa"), 75);
}

TEST_F(FuzzTest, TokenSortRatio) {
    EXPECT_EQ(fuzzywuzzy::fuzz::token_sort_ratio("fuzzy was a bear", "bear fuzzy was a"), 100);
    EXPECT_EQ(fuzzywuzzy::fuzz::token_sort_ratio("new york mets", "york new mets"), 100);
}

TEST_F(FuzzTest, TokenSetRatio) {
    EXPECT_EQ(fuzzywuzzy::fuzz::token_set_ratio("new york mets", "new york mets mets"), 100);
    EXPECT_GE(fuzzywuzzy::fuzz::token_set_ratio("new york mets", "boston red sox"), 0);
}

TEST_F(FuzzTest, UnicodeSupport) {
    std::string s1 = wstring_to_utf8(L"Московский государственный университет");
    std::string s2 = wstring_to_utf8(L"государственный университет");
    EXPECT_GE(fuzzywuzzy::fuzz::partial_ratio(s1, s2), 80);
}

TEST_F(FuzzTest, ProcessExtractOne) {
    std::vector<std::string> choices = {"Atlanta Falcons", "New York Jets", "New York Giants", "Dallas Cowboys"};
    std::string query = "new york jets";
    auto result = fuzzywuzzy::process::extractOne(query, choices, fuzzywuzzy::fuzz::ratio);
    EXPECT_EQ(result.first, "New York Jets");
    EXPECT_GE(result.second, 95);
}