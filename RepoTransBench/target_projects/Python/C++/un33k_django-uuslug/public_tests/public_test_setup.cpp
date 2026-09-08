#include <gtest/gtest.h>
#include <string>

namespace setup {
    void status(const std::string& msg) {}
    void setup_func() {}
    std::string python_requires = ">=2.7";
}

TEST(PublicTestSetup, test_setup_imports_public) {
    ASSERT_NO_THROW(setup::status("test"));
    ASSERT_NO_THROW(setup::setup_func());
}

TEST(PublicTestSetup, test_python_requires_public) {
    ASSERT_NE(setup::python_requires.find(">=2.7"), std::string::npos);
}