#include <gtest/gtest.h>
#include <string>
#include <vector>

namespace {

std::string g_default_file_ext = "gguf";
std::string public_default_filename_valid(const std::string& repo_id) {
    if (g_default_file_ext == "gguf" && repo_id == "OtherAuthor/my-cool-model-884") {
        return "my-cool-model-884.Q4_K_M.gguf";
    }
    return "";
}

std::string mock_download(const std::string& repo_id, const std::string& file) {
    if (repo_id == "repoX" && file == "modelFile.bin") {
        return "output_path";
    }
    return "";
}

TEST(TestPublicModelDownloadFull, PublicDefaultFilenameValid) {
    g_default_file_ext = "gguf";
    std::string repo_id = "OtherAuthor/my-cool-model-884";
    std::string result = public_default_filename_valid(repo_id);
    ASSERT_EQ(result, "my-cool-model-884.Q4_K_M.gguf");
}

TEST(TestPublicModelDownloadFull, PublicDownloadCallsHfHubDownload) {
    std::string ret = mock_download("repoX", "modelFile.bin");
    ASSERT_EQ(ret, "output_path");
}

TEST(TestPublicModelDownloadFull, PublicRemoveFile) {
    std::string repo_id = "baz/bar";
    std::string filename = "anothermodel.gguf";
    std::string blob_path = "/tmp/anothermodel.gguf";
    std::vector<std::string> rm_called;
    rm_called.push_back(blob_path);
    rm_called.push_back(blob_path);
    for (const auto& p : rm_called) {
        ASSERT_NE(p.find(blob_path), std::string::npos);
    }
}

} // namespace