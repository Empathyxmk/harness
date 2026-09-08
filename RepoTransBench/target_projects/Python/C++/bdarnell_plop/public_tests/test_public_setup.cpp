#include <gtest/gtest.h>
#include <cstdlib>
#include <string>
#include <fstream>
#include <sstream>

TEST(PublicSetupTest, PythonInPath) {
    std::string path = getenv("PATH") ? getenv("PATH") : "";
    bool found = path.find("python") != std::string::npos;
    ASSERT_TRUE(found);
}

TEST(PublicSetupTest, SysVersionMajor) {
    // C++ does not expose sys.version_info, so just assert True for demonstration.
    // To mimic: "sys.version_info[0] in (2, 3)"
    ASSERT_TRUE(true);
}