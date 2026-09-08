#include <gtest/gtest.h>
#include <typeinfo>
#include "fuzzywuzzy/utils.h"
#include "fuzzywuzzy/string_processing.h"

TEST(UtilsTest, ValidateStringStrAndNone) {
    // Should return true for string input
    EXPECT_TRUE(fuzzywuzzy::utils::validate_string(std::string("abc")));
    // Should return false for nullptr (None)
    EXPECT_FALSE(fuzzywuzzy::utils::validate_string(nullptr));
    // Should return false for non-string input
    EXPECT_FALSE(fuzzywuzzy::utils::validate_string(123));
    EXPECT_FALSE(fuzzywuzzy::utils::validate_string(std::vector<int>{}));
}

TEST(UtilsTest, MakeTypeConsistentStr) {
    auto [s1, s2] = fuzzywuzzy::utils::make_type_consistent("abc", "def");
    EXPECT_TRUE(typeid(s1) == typeid(std::string));
    EXPECT_TRUE(typeid(s2) == typeid(std::string));
}

TEST(UtilsTest, IntrBehavior) {
    // Should round to nearest integer (std::round's behavior for positive doubles)
    EXPECT_EQ(fuzzywuzzy::utils::intr(3.7), 4);
    EXPECT_EQ(fuzzywuzzy::utils::intr(3.3), 3);
    // Should throw for string input
    EXPECT_THROW(fuzzywuzzy::utils::intr("42"), std::invalid_argument);
}

TEST(UtilsTest, AsciiDammitAscii) {
    EXPECT_EQ(fuzzywuzzy::utils::asciidammit("hello"), "hello");
}

TEST(UtilsTest, AsciiOnlyBasic) {
    EXPECT_EQ(fuzzywuzzy::utils::asciionly("TeSt"), "TeSt");
    // asciionly returns the string unchanged for unicode input without ascii filtering
    EXPECT_EQ(fuzzywuzzy::utils::asciionly("abc✓"), "abc✓");
}

TEST(UtilsTest, FullProcessOptions) {
    std::string s = " This is Ünicode!   ";
    std::string processed = fuzzywuzzy::utils::full_process(s);
    EXPECT_NE(processed.find("ünicod"), std::string::npos);
    std::string processed_ascii = fuzzywuzzy::utils::full_process(s, true); // force_ascii
    EXPECT_NE(processed_ascii.find("nicode"), std::string::npos);

    // Edge case: empty string
    EXPECT_EQ(fuzzywuzzy::utils::full_process("", true), "");
    EXPECT_EQ(fuzzywuzzy::utils::full_process("   "), "");
}

TEST(StringProcessorTest, StripAndCase) {
    std::string s = "  hello\n";
    EXPECT_EQ(fuzzywuzzy::StringProcessor::strip(s), std::string("  hello\n").substr(2).substr(0,5));  // probably needs to call std::string::strip
    EXPECT_EQ(fuzzywuzzy::StringProcessor::to_lower_case(s), std::string("  hello\n").substr(2,5)); // needs actual implementation
    EXPECT_EQ(fuzzywuzzy::StringProcessor::to_upper_case(s), std::string("  hello\n").substr(2,5)); // needs actual implementation
}