#include <gtest/gtest.h>
#include <nlohmann/json.hpp>
#include "mnemonic/mnemonic.h"
#include <fstream>

class PublicMnemonicTest : public ::testing::Test {
protected:
    void SetUp() override {
        mnemo_en = new Mnemonic("english");
        mnemo_fr = new Mnemonic("french");
    }
    void TearDown() override {
        delete mnemo_en;
        delete mnemo_fr;
    }
    Mnemonic* mnemo_en;
    Mnemonic* mnemo_fr;
};

TEST_F(PublicMnemonicTest, PublicGenerateEntropyLengths) {
    for (int strength : {160, 192, 224, 256}) { // public test skips 128
        std::string phrase = mnemo_en->generate(strength);
        EXPECT_TRUE(!phrase.empty());
        std::istringstream iss(phrase);
        std::string w;
        while (iss >> w) {
            EXPECT_NE(std::find(mnemo_en->wordlist.begin(), mnemo_en->wordlist.end(), w), mnemo_en->wordlist.end());
        }
    }
}

TEST_F(PublicMnemonicTest, PublicGenerateInvalidStrength) {
    for (int bad : {10, 90, 270, 512}) {
        EXPECT_THROW({
            mnemo_en->generate(bad);
        }, std::invalid_argument);
    }
}

TEST_F(PublicMnemonicTest, PublicCheckValid) {
    std::string phrase = mnemo_en->generate(256);
    EXPECT_TRUE(mnemo_en->check(phrase));
}

TEST_F(PublicMnemonicTest, PublicCheckInvalid) {
    std::string phrase = "legal winner thank year wave sausage worth useful legal winner thank banana";
    EXPECT_FALSE(mnemo_en->check(phrase));
}

TEST_F(PublicMnemonicTest, PublicToMnemonicAndToEntropy) {
    std::string entropy = "ffffffffffffffffffffffffffffffff";
    std::vector<uint8_t> ent(16, 0xff);
    std::string mnemonic = mnemo_en->to_mnemonic(ent);
    EXPECT_FALSE(mnemonic.empty());
    auto recovered = mnemo_en->to_entropy(mnemonic);
    EXPECT_EQ(recovered, ent);
}

TEST_F(PublicMnemonicTest, PublicFrenchWithSpace) {
    std::string mnemonic = mnemo_fr->generate();
    EXPECT_NE(mnemonic.find(" "), std::string::npos);
}

TEST_F(PublicMnemonicTest, PublicVectors) {
    std::ifstream f("vectors.json");
    if (!f.is_open()) GTEST_SKIP() << "vectors.json not available";
    nlohmann::json vectors;
    f >> vectors;
    for (auto it = vectors.begin(); it != vectors.end(); ++it) {
        std::string lang = it.key();
        if (lang == "japanese") continue;
        Mnemonic mnemo(lang);
        int count = 0;
        for (auto& v : it.value()) {
            if (++count > 2) break;
            std::string entropy = v[0];
            std::string mnemonic_txt = v[1];
            EXPECT_TRUE(mnemo.check(mnemonic_txt));
            std::vector<uint8_t> ent(entropy.size()/2, 0);
            for (size_t i = 0; i < ent.size(); ++i)
                ent[i] = (uint8_t)strtol(entropy.substr(i*2, 2).c_str(), nullptr, 16);
            auto recovered = mnemo.to_entropy(mnemonic_txt);
            EXPECT_EQ(recovered, ent);
        }
    }
}

TEST_F(PublicMnemonicTest, PublicLanguageList) {
    auto langs = Mnemonic::list_languages();
    EXPECT_NE(std::find(langs.begin(), langs.end(), "italian"), langs.end());
    EXPECT_NE(std::find(langs.begin(), langs.end(), "spanish"), langs.end());
}

TEST_F(PublicMnemonicTest, PublicNormalizeString) {
    std::string in_str = "T͏esTing   Phrase";
    std::string out = Mnemonic::normalize_string(in_str);
    EXPECT_NE(out.find("esT"), std::string::npos);
    EXPECT_NE(out.find("Phrase"), std::string::npos);
}

TEST_F(PublicMnemonicTest, PublicExpandWord) {
    std::string prefix = "abil";
    std::string expanded = mnemo_en->expand_word(prefix);
    EXPECT_FALSE(expanded.empty());
    EXPECT_TRUE(expanded.substr(0, prefix.size()) == prefix || expanded != prefix);
}

TEST_F(PublicMnemonicTest, PublicExpand) {
    std::string phrase = "abil abou above";
    std::string expanded = mnemo_en->expand(phrase);
    EXPECT_NE(expanded.find("ability"), std::string::npos);
    EXPECT_NE(expanded.find("about"), std::string::npos);
    EXPECT_NE(expanded.find("above"), std::string::npos);
}