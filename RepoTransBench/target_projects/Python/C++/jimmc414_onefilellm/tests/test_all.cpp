#include <gtest/gtest.h>
#include <string>
#include <fstream>
#include <filesystem>
#include <vector>
#include "onefilellm.h"
#include "utils.h"

// Only new/unique tests from the second part of test_all.py append here.
// Many initial tests are already translated in previous batch.

// ----------- ALIAS SYSTEM TESTS -----------

#include <cstdlib>
#include <thread>

// We mock all alias directory locations to a temp directory to not pollute the real home
class AliasSystemTest : public ::testing::Test {
protected:
    std::filesystem::path temp_alias_dir;
    void SetUp() override {
        temp_alias_dir = std::filesystem::temp_directory_path() / std::filesystem::unique_path();
        std::filesystem::create_directory(temp_alias_dir);
        // In C++, you would inject/test the configuration or mock any static config that points to alias dir.
    }
    void TearDown() override {
        std::filesystem::remove_all(temp_alias_dir);
    }
};

TEST_F(AliasSystemTest, AliasDetection) {
    EXPECT_TRUE(is_potential_alias("myalias"));
    EXPECT_TRUE(is_potential_alias("my_alias_123"));
    EXPECT_FALSE(is_potential_alias("https://example.com"));
    EXPECT_FALSE(is_potential_alias("/path/to/file"));
    EXPECT_FALSE(is_potential_alias("C:\\Windows\\file"));
    EXPECT_FALSE(is_potential_alias("10.1234/doi"));
}

TEST_F(AliasSystemTest, AliasDirectoryCreation) {
    ensure_alias_dir_exists();
    auto alias_dir = std::filesystem::path(getenv("HOME")) / ".onefilellm_aliases";
    EXPECT_TRUE(std::filesystem::exists(alias_dir));
    EXPECT_TRUE(std::filesystem::is_directory(alias_dir));
}

TEST_F(AliasSystemTest, HandleAddAlias) {
    // Simulated console arg input
    std::vector<std::string> args = {"--add-alias", "mytest", "https://github.com/user/repo", "https://example.com"};
    // 'console' param ignored for this translation (would be rich console in Python)
    void* console = nullptr;
    bool result = handle_add_alias(args, console);
    EXPECT_TRUE(result);

    auto alias_file = temp_alias_dir / "mytest";
    EXPECT_TRUE(std::filesystem::exists(alias_file));
    std::ifstream in(alias_file);
    std::string contents((std::istreambuf_iterator<char>(in)), std::istreambuf_iterator<char>());
    EXPECT_NE(contents.find("https://github.com/user/repo"), std::string::npos);
    EXPECT_NE(contents.find("https://example.com"), std::string::npos);
}

TEST_F(AliasSystemTest, LoadAlias) {
    std::string alias_name = "testalias";
    auto alias_file = temp_alias_dir / alias_name;
    std::vector<std::string> test_targets = {"https://github.com/test/repo", "https://example.com/page"};
    std::ofstream out(alias_file);
    for (const auto& t : test_targets) out << t << "\n";
    out.close();

    void* console = nullptr;
    auto loaded_targets = load_alias(alias_name, console);
    EXPECT_EQ(loaded_targets, test_targets);
}

TEST_F(AliasSystemTest, AliasValidation) {
    void* console = nullptr;
    std::vector<std::string> invalid_names = {"test/alias", "test\\alias", "test.alias", "test:alias"};
    for (const auto& invalid_name : invalid_names) {
        std::vector<std::string> args = {"--add-alias", invalid_name, "https://example.com"};
        bool result = handle_add_alias(args, console);
        EXPECT_TRUE(result); // Should indicate error
        auto alias_file = temp_alias_dir / invalid_name;
        EXPECT_FALSE(std::filesystem::exists(alias_file));
    }
}

// ----------- INTEGRATION TESTS -----------

TEST(IntegrationTest, GithubRepoIntegration) {
    std::string repo_url = "https://github.com/jimmc414/onefilellm";
    auto result = process_github_repo(repo_url);
    EXPECT_NE(result.find("<source type=\"github_repository\""), std::string::npos);
    EXPECT_NE(result.find("README.md"), std::string::npos);
    EXPECT_NE(result.find("onefilellm.py"), std::string::npos);
}

TEST(IntegrationTest, ArxivIntegration) {
    std::string arxiv_url = "https://arxiv.org/abs/2401.14295";
    auto result = process_arxiv_pdf(arxiv_url);
    EXPECT_NE(result.find("<source type=\"arxiv\""), std::string::npos);
    EXPECT_NE(result.find("</source>"), std::string::npos);
    EXPECT_EQ(result.find("<error>"), std::string::npos);
}

TEST(IntegrationTest, YoutubeTranscriptErrorHandling) {
    std::string youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ";
    auto result = fetch_youtube_transcript(youtube_url);
    EXPECT_NE(result.find("<source type=\"youtube_transcript\""), std::string::npos);
    EXPECT_NE(result.find("</source>"), std::string::npos);
    EXPECT_NE(result.find(youtube_url), std::string::npos);

    if (result.find("<error>") != std::string::npos) {
        EXPECT_NE(result.find("<error>"), std::string::npos);
        EXPECT_NE(result.find("</error>"), std::string::npos);
    } else {
        EXPECT_GT(result.size(), 100);
    }
}

TEST(IntegrationTest, WebCrawlIntegration) {
    std::string url = "https://docs.anthropic.com/";
    auto result_map = crawl_and_extract_text(url, 1, false, true);
    EXPECT_TRUE(result_map.count("content"));
    EXPECT_TRUE(result_map.count("processed_urls"));
    EXPECT_NE(result_map["content"].find("<source type=\"web_crawl\""), std::string::npos);
    EXPECT_NE(result_map["content"].find("Anthropic"), std::string::npos);
}

// ----------- ERROR HANDLING TESTS -----------

TEST(ErrorHandling, InvalidFilePath) {
    auto result = process_text_stream("/nonexistent/file/path.txt", {"type", "stdin"}, nullptr);
    std::string low = result;
    std::transform(low.begin(), low.end(), low.begin(), ::tolower);
    EXPECT_NE(low.find("error"), std::string::npos);
}

TEST(ErrorHandling, InvalidURL) {
    auto result = process_text_stream("not_a_valid_url", {"type", "stdin"}, nullptr);
    std::string low = result;
    std::transform(low.begin(), low.end(), low.begin(), ::tolower);
    EXPECT_NE(low.find("error"), std::string::npos);
}

TEST(ErrorHandling, EmptyInput) {
    auto result = process_text_stream("", {"type", "stdin"}, nullptr);
    EXPECT_TRUE(!result.empty());
}

TEST(ErrorHandling, NetworkErrors) {
    // This would require mocking requests, for demonstration, we check that there is a content and error key
    auto result_map = crawl_and_extract_text("https://example.com", 1, false, true);
    EXPECT_TRUE(result_map.count("content"));
    EXPECT_NE(result_map["content"].find("Error processing page"), std::string::npos);
}

// ----------- PERFORMANCE TESTS -----------

TEST(PerformanceTest, LargeFileHandling) {
    // Generate large file: 1MB
    std::filesystem::path tmp = std::filesystem::temp_directory_path() / std::filesystem::unique_path();
    {
        std::ofstream f(tmp, std::ios::binary);
        for (int i = 0; i < 1024 * 1024; ++i) f << "x";
        f.close();
    }
    auto start = std::chrono::high_resolution_clock::now();
    auto result = process_text_stream(tmp.string(), {"type", "local_file"}, nullptr);
    auto end = std::chrono::high_resolution_clock::now();
    auto elapsed = std::chrono::duration_cast<std::chrono::seconds>(end - start).count();
    EXPECT_NE(result.find("<source type=\"local_file\""), std::string::npos);
    EXPECT_LT(elapsed, 5);
    std::filesystem::remove(tmp);
}
TEST(PerformanceTest, UnicodeHandling) {
    std::string content = "Hello 世界 🌍 Émojis";
    auto result = process_text_stream(content, {"type", "stdin"}, nullptr);
    EXPECT_NE(result.find(content), std::string::npos);
}
TEST(PerformanceTest, SpecialCharacters) {
    std::string special = "Special <>&\" characters";
    auto result = process_text_stream(special, {"type", "stdin"}, nullptr);
    EXPECT_NE(result.find(special), std::string::npos);
}

// ----------- CLI FUNCTIONALITY (SKETCHED for C++) -----------
// CLI-related tests in Python run the actual CLI interface; in C++ we run the analogous binary or call main() if present.
// Not implemented in this translation (would require a real CLI interface in C++), so skipping actual test implementations.