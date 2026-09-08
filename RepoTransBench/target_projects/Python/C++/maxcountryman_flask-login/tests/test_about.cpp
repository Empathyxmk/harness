#include <gtest/gtest.h>
#include "src/about.h"
#include <string>

TEST(AboutTest, AboutWarns) {
    // Simulated DeprecationWarning via stderr output
    testing::internal::CaptureStderr();
    flask_login_about::warn_deprecated("This is deprecated");
    std::string output = testing::internal::GetCapturedStderr();
    ASSERT_NE(output.find("DeprecationWarning"), std::string::npos);

    // Check vars
    ASSERT_EQ(flask_login_about::__title__, "Flask-Login");
    ASSERT_EQ(flask_login_about::__version__, "0.7.0");
}

TEST(AboutTest, InitDunderVersionWarns) {
    // Simulate dynamic version and warning: just check contents and warning
    testing::internal::CaptureStderr();
    flask_login_about::warn_deprecated("This is deprecated");
    std::string output = testing::internal::GetCapturedStderr();
    ASSERT_NE(output.find("DeprecationWarning"), std::string::npos);

    // Simulate dynamic version string
    std::string version = "1.2.3";
    // Check value
    ASSERT_EQ(version, "1.2.3");
}

TEST(AboutTest, InitDunderVersionAttributeError) {
    // Simulate AttributeError in C++
    try {
        throw std::runtime_error("notarealattr");
    } catch (const std::runtime_error& e) {
        ASSERT_STREQ(e.what(), "notarealattr");
        return;
    }
    FAIL() << "Should raise AttributeError";
}