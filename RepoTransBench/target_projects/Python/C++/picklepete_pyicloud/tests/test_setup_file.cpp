#include <gtest/gtest.h>
#include <fstream>
#include <string>
#include <stdexcept>
#include <cstdio>

class SetupFileHelper {
public:
    static bool fileExists(const std::string& filename) {
        std::ifstream ifs(filename);
        return ifs.good();
    }

    static std::string readFile(const std::string& filename) {
        std::ifstream ifs(filename);
        if (!ifs.is_open()) throw std::runtime_error("Cannot open file");
        std::string content((std::istreambuf_iterator<char>(ifs)), std::istreambuf_iterator<char>());
        return content;
    }

    static void writeFile(const std::string& filename, const std::string& content) {
        std::ofstream ofs(filename);
        if (!ofs.is_open()) throw std::runtime_error("Cannot write file");
        ofs << content;
    }

    static void removeFile(const std::string& filename) {
        std::remove(filename.c_str());
    }
};

TEST(SetupFileHelperTest, WriteReadAndRemoveFile) {
    std::string filename = "test_tempfile.txt";
    std::string data = "setup test content";

    // Write content
    SetupFileHelper::writeFile(filename, data);

    // File should exist now
    EXPECT_TRUE(SetupFileHelper::fileExists(filename));
    // Content matches
    EXPECT_EQ(SetupFileHelper::readFile(filename), data);

    // Remove the file
    SetupFileHelper::removeFile(filename);
    EXPECT_FALSE(SetupFileHelper::fileExists(filename));
}

TEST(SetupFileHelperTest, ReadingNonexistentFileThrows) {
    std::string filename = "not_there.txt";
    EXPECT_THROW(SetupFileHelper::readFile(filename), std::runtime_error);
}