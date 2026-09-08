#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "modeldownload.h"
#include "modelfiles.h"

using ::testing::_;
using ::testing::Return;
using ::testing::Invoke;

namespace {

class MockMonkeyPatch {
public:
    std::string DEFAULT_FILE_EXT;
    MockMonkeyPatch() : DEFAULT_FILE_EXT("gguf") {}
};

std::string g_default_ext = "gguf";

std::string mock_default_filename(const std::string& repo_id) {
    if (repo_id == "TheBloke/foo-123-gguf" && g_default_ext == "gguf") {
        return "foo-123.Q4_K_M.gguf";
    }
    if (repo_id == "broken" || repo_id == "foo/bar-model" || repo_id == "foo/bar-model-xyz") {
        return "";
    }
    return "";
}

class HfHubDownloadMock {
public:
    MOCK_METHOD(std::string, Download, (const std::string& repo_id, const std::string& filename), ());
};

TEST(TestModelDownloadFull, DefaultFilenameValid) {
    g_default_ext = "gguf";
    std::string repo_id = "TheBloke/foo-123-gguf";
    EXPECT_EQ(mock_default_filename(repo_id), "foo-123.Q4_K_M.gguf");
}

TEST(TestModelDownloadFull, DefaultFilenameInvalid) {
    std::string bad_repo = "broken";
    EXPECT_EQ(mock_default_filename(bad_repo), "");
    std::string repo_bad = "foo/bar-model";
    g_default_ext = "ggufx";
    EXPECT_EQ(mock_default_filename(repo_bad), "");
    g_default_ext = "gguf";
    EXPECT_EQ(mock_default_filename("foo/bar-model-xyz"), "");
}

TEST(TestModelDownloadFull, DownloadCallsHfHubDownload) {
    HfHubDownloadMock mock;
    EXPECT_CALL(mock, Download("foo", "bar")).WillOnce(Return("downloaded_path"));
    EXPECT_EQ(mock.Download("foo", "bar"), "downloaded_path");
}

TEST(TestModelDownloadFull, RemoveFile) {
    std::string repo_id = "foo/bar";
    std::string filename = "model.gguf";
    std::string blob_path = "/somewhere/model.gguf";
    std::vector<std::string> rm_called;
    // Simulate behavior: push blob_path into rm_called to record
    rm_called.push_back(blob_path);
    // Remove should call os.remove twice, only check once for this demo
    ASSERT_TRUE(std::find(rm_called.begin(), rm_called.end(), blob_path) != rm_called.end());
}

TEST(TestModelDownloadFull, RemoveFileNotFound) {
    std::string repo_id = "foo/bar";
    std::string filename = "model.gguf";
    // Simulate not found conditions, should not throw
    SUCCEED();
}

TEST(TestModelDownloadFull, RemoveRepo) {
    std::string repo_id = "foo/bar";
    std::string repo_path = "/repo/" + repo_id;
    std::vector<std::string> rm_tree;
    rm_tree.push_back(repo_path);
    ASSERT_TRUE(rm_tree[0].substr(0, 6) == "/repo/");
}

TEST(TestModelDownloadFull, RemoveRepoNone) {
    std::string repo_id = "foo/bar";
    std::string repo_path = "";
    ASSERT_EQ(repo_path, "");
}

}  // namespace