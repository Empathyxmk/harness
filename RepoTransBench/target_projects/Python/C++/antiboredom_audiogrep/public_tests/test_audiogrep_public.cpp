#include <gtest/gtest.h>
#include <fstream>
#include <string>
#include <vector>
#include <set>
#include <algorithm>

// Simulate: std::set<std::string> get_files(const std::string&, const std::vector<std::string>&);
namespace audiogrep {
    std::set<std::string> get_files(const std::string& directory, const std::vector<std::string>& exts);
}

TEST(PublicAudiogrepTest, GetFilesPublic)
{
    // Simulate creation of several files in a temp dir
    std::string tmp = "/tmp/audiogrep_pub_" + std::to_string(rand());
    system(("mkdir -p " + tmp).c_str());
    std::string a = tmp + "/file1.aac";
    std::string b = tmp + "/file2.m4a";
    std::string c = tmp + "/file3.txt";
    std::ofstream(a) << "test abc";
    std::ofstream(b) << "test abc";
    std::ofstream(c) << "test abc";
    std::set<std::string> fs = audiogrep::get_files(tmp, {".aac", ".m4a"});
    std::set<std::string> expected = {a, b};
    EXPECT_EQ(fs, expected);
    system(("rm -rf " + tmp).c_str());
}