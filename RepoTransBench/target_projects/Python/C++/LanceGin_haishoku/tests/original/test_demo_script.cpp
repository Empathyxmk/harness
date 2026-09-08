#include <gtest/gtest.h>
#include <filesystem>

TEST(TestDemoScript, demo_file_exists) {
    std::filesystem::path py = std::filesystem::current_path() / "demo" / "demo.py";
    EXPECT_TRUE(std::filesystem::exists(py));
}
TEST(TestDemoScript, demo_png_exists) {
    std::filesystem::path png = std::filesystem::current_path() / "demo" / "demo_01.png";
    EXPECT_TRUE(std::filesystem::exists(png));
}