#include <gtest/gtest.h>
#include <fstream>
#include <string>
#include <sys/stat.h>

// Helper function to check file existence using POSIX APIs
bool file_isfile(const std::string& name) {
    struct stat buffer;
    return (stat(name.c_str(), &buffer) == 0 && S_ISREG(buffer.st_mode));
}

// Public variant: test setup.py file exists using isfile instead of exists
TEST(TestPublicSetupPy, PublicSetupPyExists) {
    // Test that setup.py file exists - public variant.
    EXPECT_EQ(file_isfile("setup.py"), true);
}

// "Import" test - check can open setup.py; accept 'scm' or 'build' if present
TEST(TestPublicSetupPy, PublicImports) {
    std::ifstream infile("setup.py");
    ASSERT_TRUE(infile.is_open()) << "Cannot open setup.py for reading (file must exist).";
    try {
        std::string line;
        bool found_scm = false, found_build = false;
        while (std::getline(infile, line)) {
            if (line.find("scm") != std::string::npos ||
                line.find("SCM") != std::string::npos) {
                found_scm = true;
            }
            if (line.find("build") != std::string::npos ||
                line.find("BUILD") != std::string::npos) {
                found_build = true;
            }
        }
        // Accept either build or scm present (simulate error/exception message)
        EXPECT_TRUE(found_build || found_scm);
    } catch (const std::exception& e) {
        std::string what(e.what());
        EXPECT_TRUE(what.find("build") != std::string::npos ||
                    what.find("scm") != std::string::npos);
    }
}

// Metadata field check (public variant)
TEST(TestPublicSetupPy, PublicMetadata) {
    // Test that setup.py includes "install_requires" and "setuptools"
    std::ifstream infile("setup.py");
    ASSERT_TRUE(infile.is_open()) << "Cannot open setup.py for reading (file must exist).";
    std::string content((std::istreambuf_iterator<char>(infile)), std::istreambuf_iterator<char>());
    EXPECT_NE(content.find("install_requires"), std::string::npos);
    EXPECT_NE(content.find("setuptools"), std::string::npos);
}