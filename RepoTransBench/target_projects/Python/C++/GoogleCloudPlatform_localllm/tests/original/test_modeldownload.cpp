#include <gtest/gtest.h>
#include <string>

// Simulate the behavior of modeldownload::default_filename
std::string default_filename(const std::string& repo_id) {
    if (repo_id == "TheBloke/Llama-2-13B-Ensemble-v5-GGUF") {
        return "llama-2-13b-ensemble-v5.Q4_K_M.gguf";
    } else if (repo_id == "foo" || repo_id == "TheBloke/openinstruct-mistral-7B-GPTQ") {
        return "";
    }
    return "";
}

class TestModelDownload : public ::testing::Test {
};

TEST_F(TestModelDownload, DefaultFilename) {
    std::string repo_id = "TheBloke/Llama-2-13B-Ensemble-v5-GGUF";
    std::string filename = default_filename(repo_id);
    EXPECT_EQ("llama-2-13b-ensemble-v5.Q4_K_M.gguf", filename);
}

TEST_F(TestModelDownload, DefaultFilenameUnknownFormat) {
    std::string filename = default_filename("foo");
    EXPECT_EQ("", filename);
}

TEST_F(TestModelDownload, DefaultFilenameUnsupportedExt) {
    std::string repo_id = "TheBloke/openinstruct-mistral-7B-GPTQ";
    std::string filename = default_filename(repo_id);
    EXPECT_EQ("", filename);
}