#include <gtest/gtest.h>
#include <filesystem>
#include <chrono>
#include <unistd.h>
#include "../src/dummy_s3_pit_restore.h"

namespace fs = std::filesystem;

TEST(TestPublicS3PitRestore, GenerateTreePublic) {
    TestS3PitRestore s3pit;
    // Use public names
    std::string unique_temp_dir = "aptr_" + std::to_string(::getpid()) + "_" +
        std::to_string(std::chrono::steady_clock::now().time_since_epoch().count());
    fs::path tmpdir = fs::temp_directory_path() / unique_temp_dir;
    fs::create_directories(tmpdir);
    fs::path treepub = tmpdir / "treepub";
    fs::create_directories(treepub);

    std::vector<std::string> names = {"foo", "bar", "baz"};
    s3pit.generate_tree(treepub.string(), names);

    // Should have 3 directories, each with a file
    size_t folder_count = 0;
    for (auto& p : fs::directory_iterator(treepub)) {
        if (fs::is_directory(p)) {
            folder_count++;
            size_t file_count = 0;
            for (auto& f : fs::directory_iterator(p)) {
                if (fs::is_regular_file(f)) {
                    file_count++;
                }
            }
            EXPECT_EQ(file_count, 1);
        }
    }
    EXPECT_EQ(folder_count, 3);

    // Clean up
    fs::remove_all(tmpdir);
}