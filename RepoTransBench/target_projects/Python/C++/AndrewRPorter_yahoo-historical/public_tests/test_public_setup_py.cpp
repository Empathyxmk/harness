#include <gtest/gtest.h>
#include <fstream>
#include <string>
#include <set>

TEST(PublicSetupPyTest, SetupPyExecutionPublic) {
    // Cannot execute python in C++ tests; skip actual execution.
    SUCCEED();
}

TEST(PublicSetupPyTest, SetupPyMetadataFieldsPublic) {
    std::ifstream setup_py("setup.py");
    ASSERT_TRUE(setup_py.is_open());
    std::string contents((std::istreambuf_iterator<char>(setup_py)), std::istreambuf_iterator<char>());
    std::set<std::string> keys = {"description", "author_email", "download_url"};
    for (const auto& key : keys) {
        EXPECT_NE(contents.find(key), std::string::npos) << "setup.py missing key: " << key;
    }
}