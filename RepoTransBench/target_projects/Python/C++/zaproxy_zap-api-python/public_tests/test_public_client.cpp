#include <gtest/gtest.h>
#include <string>

// Dummy core public API for translation
namespace core {
    std::string title() {
        return "ZAP Proxy – Testing title API";
    }
    std::string banner() {
        return "Welcome to ZAP Proxy!";
    }
}

TEST(PublicClientTest, ClientTitleNewCase) {
    std::string title = core::title();
    ASSERT_GE(title.length(), 4);
}

TEST(PublicClientTest, ClientBannerNewCase) {
    std::string banner = core::banner();
    ASSERT_TRUE(banner.find("ZAP") != std::string::npos || banner.find("Proxy") != std::string::npos);
}