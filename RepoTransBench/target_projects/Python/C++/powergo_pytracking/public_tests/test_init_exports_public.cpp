#include <gtest/gtest.h>
#include "pytracking/configuration.h"
#include "pytracking/tracking.h"

using namespace pytracking;

TEST(PublicInitExports, PublicInitExportsAccess) {
    EXPECT_TRUE(dynamic_cast<Configuration*>(new Configuration()) != nullptr);
    EXPECT_TRUE(typeid(TRACKING_PIXEL) == typeid(std::vector<uint8_t>));
    EXPECT_TRUE(typeid(PNG_MIME_TYPE) == typeid(std::string));
    EXPECT_TRUE(typeid(DEFAULT_TIMEOUT_SECONDS) == typeid(int));
    // call a few exported functions to ensure callable
    EXPECT_TRUE(get_click_tracking_url);
    EXPECT_TRUE(get_click_tracking_result);
    EXPECT_TRUE(get_open_tracking_result);
    EXPECT_TRUE(get_open_tracking_url);
    EXPECT_TRUE(get_open_tracking_url_path);
    EXPECT_TRUE(get_click_tracking_url_path);
    EXPECT_TRUE(get_open_tracking_pixel);
}