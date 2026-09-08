#include <gtest/gtest.h>
#include <fstream>
#include <string>
#include <set>

// Coverage from htmlcov/z_a44f0ac069e85531_test_setup_py_py.html

TEST(SetupPyCoverageTest, SetupPyMetadataFields) {
    std::ifstream setup_py("setup.py");
    ASSERT_TRUE(setup_py.is_open());
    std::string contents((std::istreambuf_iterator<char>(setup_py)), std::istreambuf_iterator<char>());
    std::set<std::string> fields = {"author", "name", "url", "version", "packages", "install_requires"};
    for (const auto& key : fields) {
        EXPECT_NE(contents.find(key), std::string::npos) << "setup.py missing key: " << key;
    }
}
// NOTE: The execution test of setup.py is omitted for safety.