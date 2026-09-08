#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <stdexcept>
#include <memory>
#include <map>

// --- Simulated Drive Mock ---
struct FakeFile {
    std::string name;
    std::string type;
    size_t size;
    std::string date_changed;
    std::string date_modified;
    std::string date_last_open;
    bool is_folder;
    std::vector<std::shared_ptr<FakeFile>> children;
    bool has_raw;
    FakeFile* get_child(const std::string& n) {
        for (auto& c : children) if (c->name == n) return c.get();
        throw std::out_of_range("No child named '" + n + "' exists");
    }
    std::vector<std::string> dir() {
        if (!is_folder || children.empty()) {
            throw std::out_of_range("No items in folder, status: ID_INVALID");
        }
        std::vector<std::string> names;
        for (auto& c : children) names.push_back(c->name);
        return names;
    }
    std::shared_ptr<FakeFile> operator[](const std::string& n) {
        return children.size() > 0 ? children[0] : nullptr; // naive stub
    }
    struct Resp { bool raw; };
    struct Stream {
        bool raw;
        Stream(bool r): raw(r) {}
        ~Stream() {}
    };
    std::unique_ptr<Stream> open(bool /*stream*/) {
        return std::make_unique<Stream>(true);
    }
};

class PyiCloudServiceMockDrive {
public:
    // Returns the simulated root folder
    std::shared_ptr<FakeFile> root;
    PyiCloudServiceMockDrive() {
        root = std::make_shared<FakeFile>();
        root->name = "";
        root->type = "folder";
        root->size = 0;
        root->date_changed = "";
        root->date_modified = "";
        root->date_last_open = "";
        root->is_folder = true;
        // add children (simulate)
        root->children.push_back(std::make_shared<FakeFile>(FakeFile{"Keynote", "app_library", 0, "", "", "", true, {}, false}));
        root->children.push_back(std::make_shared<FakeFile>(FakeFile{"Numbers", "app_library", 0, "", "", "", true, {}, false}));
        root->children.push_back(std::make_shared<FakeFile>(FakeFile{"Pages", "folder", 0, "", "", "", true, {}, false}));
        root->children.push_back(std::make_shared<FakeFile>(FakeFile{"Preview", "app_library", 0, "", "", "", true, {}, false}));
        // pyiCloud folder
        auto pyi = std::make_shared<FakeFile>(FakeFile{"pyiCloud", "folder", 0, "", "", "", true, {}, false});
        auto test = std::make_shared<FakeFile>(FakeFile{"Test", "folder", 0, "", "", "", true, {}, false});
        // Documents
        test->children.push_back(std::make_shared<FakeFile>(FakeFile{"Document scanné 2.pdf", "file", 1024, "2020-05-03 00:16:17", "2020-05-03 00:15:17", "2020-05-03 00:24:25", false, {}, true}));
        test->children.push_back(std::make_shared<FakeFile>(FakeFile{"Scanned document 1.pdf", "file", 21644358, "2020-05-03 00:16:17", "2020-05-03 00:15:17", "2020-05-03 00:24:25", false, {}, true}));
        pyi->children.push_back(test);
        root->children.push_back(pyi);
    }
    std::shared_ptr<FakeFile> operator[](const std::string& n) {
        for (auto& c : root->children) if (c->name == n) return c;
        throw std::out_of_range("No child named '" + n + "' exists");
    }
    std::shared_ptr<FakeFile> drive = root;
};

class PyiCloudServiceMock {
public:
    PyiCloudServiceMockDrive driveMock;
    std::shared_ptr<FakeFile> drive;
    PyiCloudServiceMock() : driveMock() {
        drive = driveMock.root;
    }
    std::shared_ptr<FakeFile> operator[](const std::string& n) {
        return driveMock[n];
    }
    PyiCloudServiceMockDrive& get_driveMock() { return driveMock; }
};

#define AUTHENTICATED_USER "user"
#define VALID_PASSWORD "pass"

class DriveServiceTest : public ::testing::Test {
protected:
    std::unique_ptr<PyiCloudServiceMock> service;
    void SetUp() override { service = std::make_unique<PyiCloudServiceMock>(); }
};

TEST_F(DriveServiceTest, Root) {
    auto drive = service->drive;
    EXPECT_EQ(drive->name, "");
    EXPECT_EQ(drive->type, "folder");
    EXPECT_EQ(drive->size, 0);
    EXPECT_EQ(drive->date_changed, "");
    EXPECT_EQ(drive->date_modified, "");
    EXPECT_EQ(drive->date_last_open, "");
    auto list = drive->dir();
    std::vector<std::string> expected = {"Keynote", "Numbers", "Pages", "Preview", "pyiCloud"};
    EXPECT_EQ(list, expected);
}

TEST_F(DriveServiceTest, FolderApp) {
    auto drive = service->drive;
    FakeFile* folder = nullptr;
    for (auto& c : drive->children) if (c->name == "Preview") folder = c.get();
    ASSERT_NE(folder, nullptr);
    EXPECT_EQ(folder->name, "Preview");
    EXPECT_EQ(folder->type, "app_library");
    EXPECT_EQ(folder->size, 0);
    EXPECT_EQ(folder->date_changed, "");
    EXPECT_EQ(folder->date_modified, "");
    EXPECT_EQ(folder->date_last_open, "");
    EXPECT_THROW(folder->dir(), std::out_of_range);
}

TEST_F(DriveServiceTest, FolderNotExists) {
    auto drive = service->drive;
    EXPECT_THROW(service->get_driveMock()["not_exists"], std::out_of_range);
}

TEST_F(DriveServiceTest, Folder) {
    auto drive = service->drive;
    FakeFile* folder = nullptr;
    for (auto& c : drive->children) if (c->name == "pyiCloud") folder = c.get();
    ASSERT_NE(folder, nullptr);
    EXPECT_EQ(folder->name, "pyiCloud");
    EXPECT_EQ(folder->type, "folder");
    EXPECT_EQ(folder->size, 0);
    EXPECT_EQ(folder->date_changed, "");
    EXPECT_EQ(folder->date_modified, "");
    EXPECT_EQ(folder->date_last_open, "");
    ASSERT_FALSE(folder->children.empty());
    auto subdir = folder->dir();
    std::vector<std::string> expected = {"Test"};
    EXPECT_EQ(subdir, expected);
}

TEST_F(DriveServiceTest, Subfolder) {
    auto drive = service->drive;
    FakeFile* folder = nullptr;
    for (auto& c : drive->children) if (c->name == "pyiCloud") folder = c.get();
    ASSERT_NE(folder, nullptr);
    FakeFile* test_folder = nullptr;
    for (auto& c : folder->children) if (c->name == "Test") test_folder = c.get();
    ASSERT_NE(test_folder, nullptr);
    EXPECT_EQ(test_folder->name, "Test");
    EXPECT_EQ(test_folder->type, "folder");
    EXPECT_EQ(test_folder->size, 0);
    EXPECT_EQ(test_folder->date_changed, "");
    EXPECT_EQ(test_folder->date_modified, "");
    EXPECT_EQ(test_folder->date_last_open, "");
    auto filelist = test_folder->dir();
    std::vector<std::string> expected = {"Document scanné 2.pdf", "Scanned document 1.pdf"};
    EXPECT_EQ(filelist, expected);
}

TEST_F(DriveServiceTest, SubfolderFile) {
    auto drive = service->drive;
    FakeFile* folder = nullptr;
    for (auto& c : drive->children) if (c->name == "pyiCloud") folder = c.get();
    ASSERT_NE(folder, nullptr);
    FakeFile* test_folder = nullptr;
    for (auto& c : folder->children) if (c->name == "Test") test_folder = c.get();
    ASSERT_NE(test_folder, nullptr);
    FakeFile* file_test = nullptr;
    for (auto& c : test_folder->children) if (c->name == "Scanned document 1.pdf") file_test = c.get();
    ASSERT_NE(file_test, nullptr);
    EXPECT_EQ(file_test->name, "Scanned document 1.pdf");
    EXPECT_EQ(file_test->type, "file");
    EXPECT_EQ(file_test->size, 21644358);
    EXPECT_EQ(file_test->date_changed, "2020-05-03 00:16:17");
    EXPECT_EQ(file_test->date_modified, "2020-05-03 00:15:17");
    EXPECT_EQ(file_test->date_last_open, "2020-05-03 00:24:25");
    EXPECT_THROW(file_test->dir(), std::out_of_range);
}

TEST_F(DriveServiceTest, FileOpen) {
    auto drive = service->drive;
    FakeFile* folder = nullptr;
    for (auto& c : drive->children) if (c->name == "pyiCloud") folder = c.get();
    ASSERT_NE(folder, nullptr);
    FakeFile* test_folder = nullptr;
    for (auto& c : folder->children) if (c->name == "Test") test_folder = c.get();
    ASSERT_NE(test_folder, nullptr);
    FakeFile* file_test = nullptr;
    for (auto& c : test_folder->children) if (c->name == "Scanned document 1.pdf") file_test = c.get();
    ASSERT_NE(file_test, nullptr);
    auto resp = file_test->open(true);
    EXPECT_TRUE(resp->raw);
}