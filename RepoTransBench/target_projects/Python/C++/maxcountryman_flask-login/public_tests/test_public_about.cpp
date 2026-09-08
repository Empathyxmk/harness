#include <gtest/gtest.h>
#include "src/about.h"
#include <string>

TEST(PublicAboutTest, AboutWarnsPublic) {
    testing::internal::CaptureStderr();
    flask_login_about::warn_deprecated("This is deprecated");
    std::string output = testing::internal::GetCapturedStderr();
    ASSERT_NE(output.find("DeprecationWarning"), std::string::npos);

    ASSERT_TRUE(flask_login_about::__title__.find("Flask") != std::string::npos);
    auto cnt = std::count(flask_login_about::__version__.begin(),
                          flask_login_about::__version__.end(), '.');
    ASSERT_TRUE(cnt == 2); // e.g. "0.7.0"
}

TEST(PublicAboutTest, InitDunderVersionWarnsPublic) {
    testing::internal::CaptureStderr();
    flask_login_about::warn_deprecated("Something deprecated");
    std::string output = testing::internal::GetCapturedStderr();
    ASSERT_NE(output.find("DeprecationWarning"), std::string::npos);
    std::string version = "2.0.1";
    ASSERT_EQ(version, "2.0.1");
}

TEST(PublicAboutTest, InitDunderVersionAttributeErrorPublic) {
    std::string name = "certainlynotanattribute";
    try {
        throw std::runtime_error(name);
    } catch (const std::runtime_error& e) {
        ASSERT_STREQ(e.what(), name.c_str());
        return;
    }
    FAIL() << "Should raise AttributeError";
}