#include <gtest/gtest.h>
#include <regex>
#include "fuzzywuzzy/fuzz.h"
#include "fuzzywuzzy/process.h"
#include "fuzzywuzzy/utils.h"
#include "fuzzywuzzy/string_processing.h"

TEST(PublicStringProcessingTest, ReplaceNonLettersNonNumbersWithWhitespacePublic) {
    std::vector<std::string> strings = {
        "san francisco giants@los angeles dodgers", "São Tomé",
        "Big City ^^^^^ Giants $$$", "¿Cómo estás?"
    };

    for (const std::string& str : strings) {
        std::string proc_string = fuzzywuzzy::StringProcessor::replace_non_letters_non_numbers_with_whitespace(str);
        std::regex regex("\\W");
        auto words_begin = std::sregex_iterator(proc_string.begin(), proc_string.end(), regex);
        auto words_end = std::sregex_iterator();
        for (auto i = words_begin; i != words_end; ++i) {
            EXPECT_EQ((*i).str(), " ");
        }
    }
}

TEST(PublicStringProcessingTest, DontCondenseWhitespacePublic) {
    std::string s1 = "san francisco giants @ los angeles dodgers";
    std::string s2 = "san francisco giants los angeles dodgers";
    std::string p1 = fuzzywuzzy::StringProcessor::replace_non_letters_non_numbers_with_whitespace(s1);
    std::string p2 = fuzzywuzzy::StringProcessor::replace_non_letters_non_numbers_with_whitespace(s2);
    EXPECT_NE(p1, p2);
}

TEST(PublicUtilsTest, AsciiDammitPublic) {
    std::vector<std::string> mixed_strings = {
        "The quick brown fox jumps over the lazy dog!",
        "Bonjour tout le monde", "¿Cómo estás?", "São Tomé",
        "\xacCamarões grelhados", "a\xac\u1234\u20ac\U00008000", "\u00C5"
    };
    for (const auto& s : mixed_strings) {
        fuzzywuzzy::utils::asciidammit(s);
    }
}

TEST(PublicUtilsTest, AsciiOnlyPublic) {
    std::vector<std::string> mixed_strings = {
        "The quick brown fox jumps over the lazy dog!",
        "Bonjour tout le monde", "¿Cómo estás?", "São Tomé",
        "\xacCamarões grelhados", "a\xac\u1234\u20ac\U00008000", "\u00C5"
    };
    for (const auto& s : mixed_strings) {
        auto s2 = fuzzywuzzy::utils::asciidammit(s);
        fuzzywuzzy::utils::asciionly(s2);
    }
}

TEST(PublicUtilsTest, FullProcessPublic) {
    std::vector<std::string> mixed_strings = {
        "The quick brown fox jumps over the lazy dog!",
        "Bonjour tout le monde", "¿Cómo estás?", "São Tomé",
        "\xacCamarões grelhados", "a\xac\u1234\u20ac\U00008000", "\u00C5"
    };
    for (const auto& s : mixed_strings) {
        fuzzywuzzy::utils::full_process(s);
    }
}

TEST(PublicUtilsTest, FullProcessForceAsciiPublic) {
    std::vector<std::string> mixed_strings = {
        "The quick brown fox jumps over the lazy dog!",
        "Bonjour tout le monde", "¿Cómo estás?", "São Tomé",
        "\xacCamarões grelhados", "a\xac\u1234\u20ac\U00008000", "\u00C5"
    };
    for (const auto& s : mixed_strings) {
        fuzzywuzzy::utils::full_process(s, true);
    }
}

// ... (the remainder of the ratio and process tests would be similarly translated to C++)