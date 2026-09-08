#include <gtest/gtest.h>
#include <filesystem>
#include <chrono>
#include <unistd.h> // for getpid()
#include "../../src/dummy_s3_pit_restore.h"

namespace fs = std::filesystem;

TEST(TestS3PitRestore, GenerateTree) {
    TestS3PitRestore s3pit;
    // Simulate a temp dir using std::filesystem and C++'s temp dir
    std::string unique_temp_dir = "aptr_" + std::to_string(::getpid()) + "_" +
        std::to_string(std::chrono::steady_clock::now().time_since_epoch().count());
    fs::path tmpdir = fs::temp_directory_path() / unique_temp_dir;
    fs::create_directories(tmpdir);
    fs::path gen = tmpdir / "gen";
    fs::create_directories(gen);

    std::vector<std::string> names = {"hello", "world"};
    s3pit.generate_tree(gen.string(), names);

    // Should have 2 directories, each with a file
    size_t folder_count = 0;
    for (auto& p : fs::directory_iterator(gen)) {
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
    EXPECT_EQ(folder_count, 2);

    // Clean up
    fs::remove_all(tmpdir);
}