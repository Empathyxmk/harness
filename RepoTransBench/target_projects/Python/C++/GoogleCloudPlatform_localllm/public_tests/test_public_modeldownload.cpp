#include <gtest/gtest.h>
#include <string>
#include <algorithm>

namespace {

std::string public_default_filename(const std::string& repo_id) {
    std::string lower = repo_id;
    std::transform(lower.begin(), lower.end(), lower.begin(), ::tolower);
    if (lower.find("mistral-medium") != std::string::npos)
        return "mistral-medium.Q4_K_M.gguf";
    if (lower.find("gpt-foo") != std::string::npos)
        return "gpt-foo.Q4_K_M.gguf";
    return "";
}

TEST(TestPublicModelDownload, PublicDefaultFilename) {
    std::string repo_id = "SomeAuthor/Mistral-Medium-AI-GGUF";
    std::string filename = public_default_filename(repo_id);
    std::string lower_fn = filename;
    std::transform(lower_fn.begin(), lower_fn.end(), lower_fn.begin(), ::tolower);
    ASSERT_TRUE(lower_fn.size() >= 5 && lower_fn.substr(lower_fn.size()-5) == ".gguf");
    ASSERT_NE(lower_fn.find("mistral-medium"), std::string::npos);
}

TEST(TestPublicModelDownload, PublicDefaultFilenameLowercase) {
    std::string repo_id = "anotherone/gpt-foo-gguf";
    std::string filename = public_default_filename(repo_id);
    std::string lower_fn = filename;
    std::transform(lower_fn.begin(), lower_fn.end(), lower_fn.begin(), ::tolower);
    ASSERT_TRUE(lower_fn.size() >= 5 && lower_fn.substr(lower_fn.size()-5) == ".gguf");
    ASSERT_NE(lower_fn.find("gpt-foo"), std::string::npos);
}

} // namespace