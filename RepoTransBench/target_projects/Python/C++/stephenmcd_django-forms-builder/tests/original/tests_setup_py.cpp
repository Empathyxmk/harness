#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <algorithm>
#include <filesystem>
#include <fstream>

namespace fs = std::filesystem;

TEST(SetupPy, ExcludeFiles) {
    // Simlulate creating dummy files and removing them based on exclusions
    fs::path tmp_dir = fs::temp_directory_path() / "forms_builder_cpp_test";
    fs::create_directories(tmp_dir);

    fs::path py_file = tmp_dir / "tmp.py";
    fs::path other_file = tmp_dir / "tmp.txt";
    fs::path pyc_file = tmp_dir / "tmp.pyc";

    std::ofstream(py_file) << "pass";
    std::ofstream(other_file) << "hello";
    std::ofstream(pyc_file) << "compiled!";

    std::vector<fs::path> files = {py_file, other_file, pyc_file};
    std::vector<fs::path> exclude = {py_file, other_file};

    // Simulate exclusion/removal
    for (auto& f : exclude) {
        fs::remove(f);
    }
    // Only pyc should remain
    EXPECT_TRUE(fs::exists(pyc_file));
    EXPECT_FALSE(fs::exists(py_file));
    EXPECT_FALSE(fs::exists(other_file));
    fs::remove_all(tmp_dir);
}

TEST(SetupPy, RemoveBuild) {
    fs::path tmp_dir = fs::temp_directory_path() / "forms_builder_cpp_test2";
    fs::create_directories(tmp_dir);
    fs::path build_dir = tmp_dir / "build";
    fs::create_directories(build_dir);
    EXPECT_TRUE(fs::exists(build_dir));
    // Simulate rmtree(build/)
    fs::remove_all(build_dir);
    EXPECT_FALSE(fs::exists(build_dir));
    fs::remove_all(tmp_dir);
}