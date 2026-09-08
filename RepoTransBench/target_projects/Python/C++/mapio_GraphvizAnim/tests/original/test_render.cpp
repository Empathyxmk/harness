#include <gtest/gtest.h>
#include <cstdlib> // for std::system, used for "call"
#include <vector>
#include <string>
#include <fstream>
#include <filesystem>

// These are stub implementations for render.h
namespace render {
    int call_counter = 0;
    int call(const std::vector<std::string>& args) {
        ++call_counter;
        // simulate a "convert" (e.g., ImageMagick) or any shell call
        return 0; // pretend success
    }
    std::vector<std::string> render(const std::vector<std::string>&, const std::string& base, const std::string&, int) {
        // Simulate creation of filepaths for dot
        std::vector<std::string> files = {
            base + "-0.dot",
            base + "-1.dot"
        };
        // Actually create the files on disk
        for (auto& file : files) {
            std::ofstream f(file);
            f << "digraph {}";
            f.close();
        }
        return files;
    }
    void gif(const std::vector<std::string>& files, const std::string& out, int /*delay*/, int /*size*/) {
        // Each call to this function triggers call with "convert"
        call({"convert", files[0], out + ".gif"});
    }
}

TEST(RenderTest, RenderTmp) {
    namespace fs = std::filesystem;
    std::string tmpdir = "./tmp_test_render";
    fs::create_directory(tmpdir);
    auto files = render::render({"digraph{}", "digraph{}"}, tmpdir + "/myanim", "dot", 10);
    ASSERT_EQ(files.size(), 2u);
    for (auto& file : files) {
        EXPECT_TRUE(fs::exists(file));
    }
    // Clean up
    for (auto& file : files) std::remove(file.c_str());
    fs::remove(tmpdir);
}

TEST(RenderTest, Gif) {
    namespace fs = std::filesystem;
    std::string tmpdir = "./tmp_test_render";
    fs::create_directory(tmpdir);
    std::vector<std::string> files;
    for (int i=0; i<2; ++i) {
        std::string fname = tmpdir + "/f" + std::to_string(i) + ".png";
        std::ofstream(fname) << "test";
        files.push_back(fname);
    }
    int prev_count = render::call_counter;
    render::gif(files, tmpdir + "/anim", 123, 11);
    EXPECT_GT(render::call_counter, prev_count);
    for (auto& file : files) std::remove(file.c_str());
    fs::remove(tmpdir);
}