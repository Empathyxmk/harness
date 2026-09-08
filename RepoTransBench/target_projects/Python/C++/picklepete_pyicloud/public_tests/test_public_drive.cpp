#include <gtest/gtest.h>
#include <stdexcept>
#include <string>
#include <vector>
#include <algorithm>

// Simulate a minimal Drive representation for testing
struct DriveFile {
    std::string name;
    size_t size;
    bool is_folder;
};

class PublicDriveMock {
public:
    explicit PublicDriveMock() : files_({
        {"README.md", 128, false},
        {"Main Folder", 0, true},
        {"photo.jpg", 800, false}
    }) {}

    std::vector<DriveFile> listFiles() const {
        return files_;
    }

    DriveFile getFile(const std::string& name) const {
        auto it = std::find_if(files_.begin(), files_.end(), [&](const DriveFile& f) { return f.name == name; });
        if (it == files_.end()) throw std::runtime_error("File not found");
        return *it;
    }

    size_t totalFiles() const {
        return files_.size();
    }
private:
    std::vector<DriveFile> files_;
};

TEST(PublicDriveTest, ListFilesReturnsAll) {
    PublicDriveMock drive;
    auto files = drive.listFiles();
    EXPECT_EQ(files.size(), 3);
    EXPECT_EQ(files[0].name, "README.md");
    EXPECT_TRUE(files[1].is_folder);
}

TEST(PublicDriveTest, GetFileByName) {
    PublicDriveMock drive;
    auto f = drive.getFile("photo.jpg");
    EXPECT_EQ(f.name, "photo.jpg");
    EXPECT_EQ(f.size, 800);
    EXPECT_FALSE(f.is_folder);
}

TEST(PublicDriveTest, GetFileThrowsIfNotFound) {
    PublicDriveMock drive;
    EXPECT_THROW(drive.getFile("notreal.txt"), std::runtime_error);
}

TEST(PublicDriveTest, ReportsTotalFiles) {
    PublicDriveMock drive;
    EXPECT_EQ(drive.totalFiles(), 3);
}