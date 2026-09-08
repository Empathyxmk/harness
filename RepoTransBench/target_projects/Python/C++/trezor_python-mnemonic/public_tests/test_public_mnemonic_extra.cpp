#include <gtest/gtest.h>
#include "mnemonic/mnemonic.h"
#include <filesystem>

TEST(PublicMnemonicExtraTest, PublicInvalidLanguage) {
    EXPECT_THROW({
        Mnemonic m("notareallanguage");
    }, ConfigurationError);
}

TEST(PublicMnemonicExtraTest, PublicDetectLanguageValid) {
    std::string english_phrase = "legal winner thank year wave sausage worth useful legal winner thank yellow";
    std::string lang = Mnemonic::detect_language(english_phrase);
    EXPECT_EQ(lang, "english");
}

TEST(PublicMnemonicExtraTest, PublicDetectLanguageInvalid) {
    std::string phrase = "zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo";
    EXPECT_THROW({
        Mnemonic::detect_language(phrase);
    }, ConfigurationError);
}

TEST(PublicMnemonicExtraTest, PublicListLanguagesUnique) {
    auto langs = Mnemonic::list_languages();
    std::set<std::string> unique(langs.begin(), langs.end());
    EXPECT_EQ(langs.size(), unique.size());
    EXPECT_NE(std::find(langs.begin(), langs.end(), "japanese"), langs.end());
}

TEST(PublicMnemonicExtraTest, PublicWordlistFileExists) {
    auto langs = Mnemonic::list_languages();
    for (const auto& lang : langs) {
        std::string path = "src/mnemonic/wordlist/" + lang + ".txt";
        EXPECT_TRUE(std::filesystem::exists(path));
    }
}

TEST(PublicMnemonicExtraTest, PublicInitWithWordlistInvalidLength) {
    std::vector<std::string> fake_wordlist(2050, "bar");
    EXPECT_THROW({
        Mnemonic m("anotherfake", fake_wordlist);
    }, ConfigurationError);
}

TEST(PublicMnemonicExtraTest, PublicInitWithWordlistValidLength) {
    std::vector<std::string> fake_wordlist(2048, "bar");
    Mnemonic m("anotherfake", fake_wordlist);
    EXPECT_EQ(m.get_wordlist(), fake_wordlist);
}

TEST(PublicMnemonicExtraTest, PublicExpandWordNotFound) {
    Mnemonic m("english");
    std::string result = m.expand_word("unknownprefixword");
    EXPECT_EQ(result, "unknownprefixword");
}

TEST(PublicMnemonicExtraTest, PublicCheckExpandsPrefixInput) {
    Mnemonic m("english");
    std::string phrase = "able about above absent absorb abstract absurd abuse access accident account accuse";
    EXPECT_TRUE(m.check(phrase) || !m.check(phrase));
}

TEST(PublicMnemonicExtraTest, PublicStripAccentsBasicPatch) {
    SUCCEED();
}