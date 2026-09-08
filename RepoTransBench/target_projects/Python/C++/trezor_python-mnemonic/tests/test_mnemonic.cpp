#include <gtest/gtest.h>
#include "mnemonic/mnemonic.h"
#include <fstream>
#include <nlohmann/json.hpp>

class MnemonicTest : public ::testing::Test {
protected:
    void SetUp() override {
        mnemo_en = new Mnemonic("english");
        mnemo_jp = new Mnemonic("japanese");
    }
    void TearDown() override {
        delete mnemo_en;
        delete mnemo_jp;
    }
    Mnemonic* mnemo_en;
    Mnemonic* mnemo_jp;
};

TEST_F(MnemonicTest, GenerateEntropyLengths) {
    for (int strength : {128, 160, 192, 224, 256}) {
        std::string phrase = mnemo_en->generate(strength);
        EXPECT_TRUE(!phrase.empty());
        std::istringstream iss(phrase);
        std::string w;
        while (iss >> w) {
            EXPECT_NE(std::find(mnemo_en->wordlist.begin(), mnemo_en->wordlist.end(), w), mnemo_en->wordlist.end());
        }
    }
}

TEST_F(MnemonicTest, GenerateInvalidStrength) {
    for (int bad : {0, 132, 300, 1000}) {
        EXPECT_THROW({
            mnemo_en->generate(bad);
        }, std::invalid_argument);
    }
}

TEST_F(MnemonicTest, CheckValid) {
    std::string phrase = mnemo_en->generate(128);
    EXPECT_TRUE(mnemo_en->check(phrase));
}

TEST_F(MnemonicTest, CheckInvalid) {
    std::string phrase = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon wrong";
    EXPECT_FALSE(mnemo_en->check(phrase));
}

TEST_F(MnemonicTest, ToMnemonicAndToEntropy) {
    std::string entropy = "00000000000000000000000000000000";
    std::vector<uint8_t> ent(16, 0x00);
    std::string mnemonic = mnemo_en->to_mnemonic(ent);
    EXPECT_FALSE(mnemonic.empty());
    auto recovered = mnemo_en->to_entropy(mnemonic);
    EXPECT_EQ(recovered, ent);
}

TEST_F(MnemonicTest, JapaneseNoSpace) {
    std::string mnemonic = mnemo_jp->generate();
    // BIP39 Japanese uses ideographic space; mimicked here by containing a space
    EXPECT_NE(mnemonic.find("\u3000"), std::string::npos);
}

TEST_F(MnemonicTest, Vectors) {
    std::ifstream f("vectors.json");
    if (!f.is_open()) GTEST_SKIP() << "vectors.json not available";
    nlohmann::json vectors;
    f >> vectors;
    for (auto it = vectors.begin(); it != vectors.end(); ++it) {
        std::string lang = it.key();
        if (lang == "japanese") continue;
        Mnemonic mnemo(lang);
        for (auto& v : it.value()) {
            std::string entropy = v[0];
            std::string mnemonic_txt = v[1];
            EXPECT_TRUE(mnemo.check(mnemonic_txt));
            std::vector<uint8_t> ent(entropy.size()/2, 0);
            for (size_t i = 0; i < ent.size(); ++i)
                ent[i] = (uint8_t) strtol(entropy.substr(i*2, 2).c_str(), nullptr, 16);
            auto recovered = mnemo.to_entropy(mnemonic_txt);
            EXPECT_EQ(recovered, ent);
        }
    }
}

TEST_F(MnemonicTest, LanguageList) {
    auto langs = Mnemonic::list_languages();
    EXPECT_NE(std::find(langs.begin(), langs.end(), "english"), langs.end());
    EXPECT_NE(std::find(langs.begin(), langs.end(), "french"), langs.end());
}

TEST_F(MnemonicTest, NormalizeString) {
    std::string in_str = "E͏xample   String";
    std::string out = Mnemonic::normalize_string(in_str);
    EXPECT_NE(out.find("xample"), std::string::npos);
    EXPECT_NE(out.find("String"), std::string::npos);
}

TEST_F(MnemonicTest, ExpandWord) {
    std::string prefix = "aban";
    std::string expanded = mnemo_en->expand_word(prefix);
    EXPECT_FALSE(expanded.empty());
    EXPECT_EQ(expanded.substr(0, prefix.size()), prefix);
}

TEST_F(MnemonicTest, Expand) {
    std::string phrase = "aban abou above";
    std::string expanded = mnemo_en->expand(phrase);
    EXPECT_NE(expanded.find("abandon"), std::string::npos);
    EXPECT_NE(expanded.find("about"), std::string::npos);
    EXPECT_NE(expanded.find("above"), std::string::npos);
}