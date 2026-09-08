#include <gtest/gtest.h>
#include <fstream>
#include <string>
#include <set>

// From htmlcov/d_a44f0ac069e85531_test_setup_py_py.html

// Note: The Python test 'test_setup_py_execution(monkeypatch)' covers executing setup.py with a monkeypatched setup()
// In C++, running/patching/monkeypatching Python setup.py is not idiomatic, so we focus on fields only.

TEST(SetupPyHtmlcovTest, SetupPyMetadataFields) {
    std::ifstream setup_py("setup.py");
    ASSERT_TRUE(setup_py.is_open()) << "Cannot open setup.py";
    std::string contents((std::istreambuf_iterator<char>(setup_py)), std::istreambuf_iterator<char>());
    std::set<std::string> fields = {"author", "name", "url", "version", "packages", "install_requires"};
    for (const auto& key : fields) {
        EXPECT_NE(contents.find(key), std::string::npos) << "setup.py missing key: " << key;
    }
}