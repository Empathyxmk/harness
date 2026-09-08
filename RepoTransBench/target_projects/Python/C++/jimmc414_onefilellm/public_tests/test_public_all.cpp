#include <gtest/gtest.h>
#include <string>
#include <fstream>
#include <filesystem>
#include "utils.h"

namespace fs = std::filesystem;

class PublicTestUtilityFunctions : public ::testing::Test {
protected:
    fs::path tmpd;
    void SetUp() override { 
        tmpd = fs::temp_directory_path() / fs::unique_path(); 
        fs::create_directory(tmpd);
    }
    void TearDown() override {
        fs::remove_all(tmpd);
    }
};

TEST_F(PublicTestUtilityFunctions, SafeFileReadPublic) {
    std::string f_utf8 = (tmpd / "abc.txt").string();
    {
        std::ofstream f(f_utf8, std::ios::binary);
        f << "Public 测试";
    }
    std::string content = utils::safe_file_read(f_utf8);
    EXPECT_EQ(content, "Public 测试");

    std::string f_latin1 = (tmpd / "latinpublic.txt").string();
    std::ofstream f2(f_latin1, std::ios::binary);
    f2.write("ma\xf1ana", 7);
    f2.close();
    EXPECT_EQ(utils::safe_file_read(f_latin1), "mañana");
}

TEST_F(PublicTestUtilityFunctions, FileExtensionDetectionPublic) {
    EXPECT_EQ(utils::get_file_extension("some.JS"), ".js");
    EXPECT_EQ(utils::get_file_extension("archive.TAR.GZ"), ".gz");
    EXPECT_EQ(utils::get_file_extension("README"), "");
    EXPECT_EQ(utils::get_file_extension("dots.with.many.parts.doc"), ".doc");
}

TEST_F(PublicTestUtilityFunctions, IsBinaryFilePublic) {
    std::string t_file = (tmpd / "t.txt").string();
    {
        std::ofstream f(t_file, std::ios::binary);
        f << "Sample text";
    }
    EXPECT_FALSE(utils::is_binary_file(t_file));
    std::string b_file = (tmpd / "b.dat").string();
    {
        std::ofstream f(b_file, std::ios::binary);
        char arr[4] = {(char)0xff, (char)0xd8, (char)0xff, (char)0xdb};
        f.write(arr, 4);
    }
    EXPECT_TRUE(utils::is_binary_file(b_file));
}

TEST_F(PublicTestUtilityFunctions, IsExcludedFilePublic) {
    EXPECT_TRUE(utils::is_excluded_file("dist/bundle.js"));
    EXPECT_TRUE(utils::is_excluded_file(".git/hooks/pre-commit"));
    EXPECT_TRUE(utils::is_excluded_file("lib.min.js"));
    EXPECT_TRUE(utils::is_excluded_file("__pycache__/something.pyc"));
    EXPECT_TRUE(utils::is_excluded_file("node_modules/module.js"));
    EXPECT_FALSE(utils::is_excluded_file("main.c"));
    EXPECT_FALSE(utils::is_excluded_file("script.rb"));
}

TEST_F(PublicTestUtilityFunctions, IsAllowedFiletypePublic) {
    EXPECT_TRUE(utils::is_allowed_filetype("index.html"));
    EXPECT_TRUE(utils::is_allowed_filetype("data.csv"));
    EXPECT_TRUE(utils::is_allowed_filetype("setup.py"));
    EXPECT_FALSE(utils::is_allowed_filetype("archive.tar.gz"));
    EXPECT_FALSE(utils::is_allowed_filetype("some.dll"));
    EXPECT_FALSE(utils::is_allowed_filetype("compressed.rar"));
}

TEST_F(PublicTestUtilityFunctions, UrlUtilitiesPublic) {
    std::string base = "https://public.com/section/";
    EXPECT_TRUE(utils::is_same_domain(base, "https://public.com/else/"));
    EXPECT_FALSE(utils::is_same_domain(base, "https://alt.com/test/"));
    EXPECT_TRUE(utils::is_within_depth(base, "https://public.com/section/page2", 1));
    EXPECT_TRUE(utils::is_within_depth(base, "https://public.com/section/inner/page", 2));
    EXPECT_FALSE(utils::is_within_depth(base, "https://public.com/section/a/b/d", 2));
}

TEST_F(PublicTestUtilityFunctions, EscapeXmlPublic) {
    std::string x = "<publicTest>More & stuff</publicTest>";
    EXPECT_EQ(utils::escape_xml(x), x);
}