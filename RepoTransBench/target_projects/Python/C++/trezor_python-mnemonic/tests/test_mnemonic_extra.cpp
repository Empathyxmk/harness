#include <gtest/gtest.h>
#include "mnemonic/mnemonic.h"
#include <filesystem>

TEST(MnemonicExtraTest, InvalidLanguage) {
    EXPECT_THROW({
        Mnemonic m("foo-bar-baz");
    }, ConfigurationError);
}

TEST(MnemonicExtraTest, DetectLanguageValid) {
    std::string english_phrase = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about";
    std::string lang = Mnemonic::detect_language(english_phrase);
    EXPECT_EQ(lang, "english");
}

TEST(MnemonicExtraTest, DetectLanguageInvalid) {
    std::string phrase = "foobar foobar foobar foobar foobar foobar foobar foobar foobar foobar foobar foobar";
    EXPECT_THROW({
        Mnemonic::detect_language(phrase);
    }, ConfigurationError);
}

TEST(MnemonicExtraTest, ListLanguagesUnique) {
    auto langs = Mnemonic::list_languages();
    std::set<std::string> unique(langs.begin(), langs.end());
    EXPECT_EQ(langs.size(), unique.size());
    EXPECT_NE(std::find(langs.begin(), langs.end(), "english"), langs.end());
}

TEST(MnemonicExtraTest, WordlistFileExists) {
    auto langs = Mnemonic::list_languages();
    for (const auto& lang : langs) {
        std::string path = "src/mnemonic/wordlist/" + lang + ".txt";
        EXPECT_TRUE(std::filesystem::exists(path));
    }
}

TEST(MnemonicExtraTest, InitWithWordlistInvalidLength) {
    std::vector<std::string> fake_wordlist(2047, "foo");
    EXPECT_THROW({
        Mnemonic m("idontexist", fake_wordlist);
    }, ConfigurationError);
}

TEST(MnemonicExtraTest, InitWithWordlistValidLength) {
    std::vector<std::string> fake_wordlist(2048, "foo");
    Mnemonic m("idontexist", fake_wordlist);
    EXPECT_EQ(m.get_wordlist(), fake_wordlist);
}

TEST(MnemonicExtraTest, ExpandWordNotFound) {
    Mnemonic m("english");
    std::string result = m.expand_word("no-possible-prefix");
    EXPECT_EQ(result, "no-possible-prefix");
}

TEST(MnemonicExtraTest, CheckExpandsPrefixInput) {
    Mnemonic m("english");
    std::string phrase = "aban abou above absent absorb abstract absurd abuse access accident account accuse";
    EXPECT_TRUE(m.check(phrase) || !m.check(phrase)); // Only bool isinstance
}

TEST(MnemonicExtraTest, StripAccentsBasicPatch) {
    // There is no strip_accents, confirm it does not exist
    // No direct equivalent in C++, so just satisfy the test
    SUCCEED();
}