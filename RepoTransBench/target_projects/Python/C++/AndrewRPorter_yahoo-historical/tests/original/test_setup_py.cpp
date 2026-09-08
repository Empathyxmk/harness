#include <gtest/gtest.h>
#include <fstream>
#include <string>
#include <set>

TEST(SetupPyTest, SetupPyMetadataFields) {
    std::ifstream setup_py("setup.py");
    ASSERT_TRUE(setup_py.is_open());
    std::string contents((std::istreambuf_iterator<char>(setup_py)), std::istreambuf_iterator<char>());
    std::set<std::string> fields = {"author", "name", "url", "version", "packages", "install_requires"};
    for (const auto& key : fields) {
        EXPECT_NE(contents.find(key), std::string::npos) << "setup.py missing key: " << key;
    }
}
// We omit execution of setup.py for safety/compat.