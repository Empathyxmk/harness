// Translated from tests/test_binaries.py
#include <gtest/gtest.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <random>
#include <filesystem>
#include <cstdio>
#include <string>
#include <vector>
#include <tuple>
#include <stdexcept>
#include <cstdlib>

// NOTE: These are dummy/mock replacements for Python fairseq modules.
// Real fairseq binary calls would be via subprocess or CLI, typically
// for this kind of system test.

namespace fairseq_cli {
    void preprocess(const std::string& args) {
        // Placeholder: simulate CLI call, e.g., system("./fairseq-preprocess ...");
        // Should actually call the right command or API.
    }
    void train(const std::string& args) {}
    void generate(const std::string& args) {}
    void interactive(const std::string& args) {}
    void eval_lm(const std::string& args) {}
    void validate(const std::string& args) {}
}

// Helper to get temp directory, simulate tempfile.TemporaryDirectory
class ScopedTempDir {
    std::string path_;
public:
    ScopedTempDir(const std::string& prefix) {
        char templ[256];
        snprintf(templ, sizeof(templ), "/tmp/%s_XXXXXX", prefix.c_str());
        char* tmpdir = mkdtemp(templ);
        ASSERT_TRUE(tmpdir != nullptr);
        path_ = std::string(tmpdir);
    }
    ~ScopedTempDir() {
        std::filesystem::remove_all(path_);
    }
    const std::string& path() const { return path_; }
};

// Simulate dummy dataset writing, random txt files
void create_dummy_data(const std::string& dir, int num_examples=100, int maxlen=20, bool alignment=false) {
    auto randchar = []() -> char { return (char)('a' + rand()%26); };
    auto make_file = [&](const char* fname) {
        std::ofstream ofs(dir + "/" + fname);
        for (int i=0; i<num_examples; ++i) {
            int len = 1 + (rand() % maxlen);
            for (int j=0; j<len; ++j) {
                ofs << randchar();
                if (j != len-1) ofs << " ";
            }
            ofs << "\n";
        }
    };
    make_file("train.in");
    make_file("train.out");
    make_file("valid.in");
    make_file("valid.out");
    make_file("test.in");
    make_file("test.out");
    // Skipping real alignments
}

void preprocess_translation_data(const std::string& dir, const std::vector<std::string>& extra_flags={}) {
    // Placeholder for fairseq preprocess
    // Would form a CLI string and call fairseq_cli::preprocess(args)
}
void train_translation_model(const std::string& dir, const std::string& arch, const std::vector<std::string>& extra_flags={},
                            const std::string& task="translation", bool run_validation=false,
                            const std::vector<std::string>& lang_flags={"--source-lang", "in", "--target-lang", "out"},
                            const std::vector<std::string>& extra_valid_flags={}) {
    // Simulate model training
}
void generate_main(const std::string& dir, const std::vector<std::string>& extra_flags={}) {
    // Simulate generate and interactive
}
void preprocess_lm_data(const std::string& dir) {
    // Simulate LM preprocess
}
void train_language_model(const std::string& dir, const std::string& arch, const std::vector<std::string>& extra_flags={}, bool run_validation=false) {
    // Simulate train LM
}
void eval_lm_main(const std::string& dir) {
    // Simulate eval_lm
}

// --- Tests ---

class TestTranslation : public ::testing::Test {
protected:
    void SetUp() override {}
    void TearDown() override {}

public:
    TEST_F(TestTranslation, test_fconv) {
        ScopedTempDir tmpdir("test_fconv");
        create_dummy_data(tmpdir.path());
        preprocess_translation_data(tmpdir.path());
        train_translation_model(tmpdir.path(), "fconv_iwslt_de_en");
        generate_main(tmpdir.path());
    }
    TEST_F(TestTranslation, test_raw) {
        ScopedTempDir tmpdir("test_fconv_raw");
        create_dummy_data(tmpdir.path());
        preprocess_translation_data(tmpdir.path(), {"--dataset-impl", "raw"});
        train_translation_model(tmpdir.path(), "fconv_iwslt_de_en", {"--dataset-impl", "raw"});
        generate_main(tmpdir.path(), {"--dataset-impl", "raw"});
    }
    TEST_F(TestTranslation, test_update_freq) {
        ScopedTempDir tmpdir("test_update_freq");
        create_dummy_data(tmpdir.path());
        preprocess_translation_data(tmpdir.path());
        train_translation_model(tmpdir.path(), "fconv_iwslt_de_en", {"--update-freq", "3"});
        generate_main(tmpdir.path());
    }
};

class TestStories : public ::testing::Test {
    void SetUp() override {}
    void TearDown() override {}
public:
    TEST_F(TestStories, test_fconv_self_att_wp) {
        ScopedTempDir tmpdir("test_fconv_self_att_wp");
        create_dummy_data(tmpdir.path());
        preprocess_translation_data(tmpdir.path());
        std::vector<std::string> config = {
            "--encoder-layers", "[(128,3)]*2",
            "--decoder-layers", "[(128,3)]*2",
            "--decoder-attention", "True",
            "--encoder-attention", "False",
            "--gated-attention", "True",
            "--self-attention", "True",
            "--project-input", "True",
            "--encoder-embed-dim", "8",
            "--decoder-embed-dim", "8",
            "--decoder-out-embed-dim", "8",
            "--multihead-self-attention-nheads", "2"
        };
        train_translation_model(tmpdir.path(), "fconv_self_att_wp", config);
        generate_main(tmpdir.path());

        // Fusion model (simulate checkpoint copy and new train)
        std::filesystem::rename(tmpdir.path()+"/checkpoint_last.pt", tmpdir.path()+"/pretrained.pt");
        config.push_back("--pretrained");
        config.push_back("True");
        config.push_back("--pretrained-checkpoint");
        config.push_back(tmpdir.path()+"/pretrained.pt");
        config.push_back("--save-dir");
        config.push_back(tmpdir.path()+"/fusion_model");
        train_translation_model(tmpdir.path(), "fconv_self_att_wp", config);
    }
};

class TestLanguageModeling : public ::testing::Test {
    void SetUp() override {}
    void TearDown() override {}
public:
    TEST_F(TestLanguageModeling, test_fconv_lm) {
        ScopedTempDir tmpdir("test_fconv_lm");
        create_dummy_data(tmpdir.path());
        preprocess_lm_data(tmpdir.path());
        train_language_model(tmpdir.path(), "fconv_lm", {
            "--decoder-layers", "[(850, 3)] * 2 + [(1024,4)]",
            "--decoder-embed-dim", "280",
            "--optimizer", "nag",
            "--lr", "0.1"
        });
        eval_lm_main(tmpdir.path());
    }
    TEST_F(TestLanguageModeling, test_transformer_lm) {
        ScopedTempDir tmpdir("test_transformer_lm");
        create_dummy_data(tmpdir.path());
        preprocess_lm_data(tmpdir.path());
        train_language_model(tmpdir.path(), "transformer_lm", {"--add-bos-token"}, true);
        eval_lm_main(tmpdir.path());
        generate_main(tmpdir.path(), {"--task", "language_modeling", "--sample-break-mode", "eos", "--tokens-per-sample", "500"});
    }
    TEST_F(TestLanguageModeling, test_lightconv_lm) {
        ScopedTempDir tmpdir("test_lightconv_lm");
        create_dummy_data(tmpdir.path());
        preprocess_lm_data(tmpdir.path());
        train_language_model(tmpdir.path(), "lightconv_lm", {"--add-bos-token"}, true);
        eval_lm_main(tmpdir.path());
        generate_main(tmpdir.path(), {"--task", "language_modeling", "--sample-break-mode", "eos", "--tokens-per-sample", "500"});
    }
    TEST_F(TestLanguageModeling, test_lstm_lm) {
        ScopedTempDir tmpdir("test_lstm_lm");
        create_dummy_data(tmpdir.path());
        preprocess_lm_data(tmpdir.path());
        train_language_model(tmpdir.path(), "lstm_lm", {"--add-bos-token"}, true);
        eval_lm_main(tmpdir.path());
        generate_main(tmpdir.path(), {"--task", "language_modeling", "--sample-break-mode", "eos", "--tokens-per-sample", "500"});
    }
};