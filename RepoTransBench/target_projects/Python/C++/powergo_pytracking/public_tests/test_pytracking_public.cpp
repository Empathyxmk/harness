#include <gtest/gtest.h>
#include "pytracking/configuration.h"
#include "pytracking/tracking.h"
using namespace pytracking;

const std::string ALT_URL_TO_TRACK = "https://anotherdomain.io/tracking/?data=newdata";
const std::string ALT_BASE_CLICK_TRACKING_URL = "https://y.z.com/track/";
const std::string ALT_BASE_OPEN_TRACKING_URL = "https://y.z.com/track/open/";
const std::string ALT_WEBHOOK_URL = "https://notify.me/webhook/";

std::map<std::string, util::Any> ALT_METADATA = {
    {"param4", "val4"},
    {"another", true},
    {"nested_alt", std::map<std::string, util::Any>{{"paramA", "valA"}}}
};
std::map<std::string, util::Any> ALT_DEFAULT_METADATA = {
    {"key42", false},
    {"strangeé", "winoèèè"},
    {"paramX", "other3"}
};
std::map<std::string, util::Any> ALT_EXPECTED_METADATA = []{
    auto m = ALT_DEFAULT_METADATA;
    m.insert(ALT_METADATA.begin(), ALT_METADATA.end());
    return m;
}();
std::map<std::string, util::Any> ALT_REQUEST_DATA = {
    {"user_agent", "Safari"},
    {"user_ip", "192.168.1.1"}
};

Configuration ALT_CONFIGURATION(
    ALT_WEBHOOK_URL,
    ALT_BASE_OPEN_TRACKING_URL,
    ALT_BASE_CLICK_TRACKING_URL,
    ALT_DEFAULT_METADATA
);

TEST(PublicPyTracking, PublicGetOpenTrackingPixel) {
    auto [pixel, mime] = get_open_tracking_pixel();
    EXPECT_TRUE(typeid(pixel) == typeid(std::vector<uint8_t>));
    EXPECT_EQ(mime, "image/png");
}
TEST(PublicPyTracking, PublicBasicGetOpenTrackingUrl) {
    auto url = get_open_tracking_url(ALT_BASE_OPEN_TRACKING_URL);
    EXPECT_TRUE(url.find(ALT_BASE_OPEN_TRACKING_URL) == 0);
    EXPECT_NE(url.substr(ALT_BASE_OPEN_TRACKING_URL.length()), "");
}
TEST(PublicPyTracking, PublicBasicGetOpenTrackingUrlAppendSlash) {
    auto url = get_open_tracking_url(ALT_BASE_OPEN_TRACKING_URL, true);
    EXPECT_TRUE(url.rfind("/") == (url.length() - 1));
}
TEST(PublicPyTracking, PublicInConfigOpenTrackingUrl) {
    auto url = get_open_tracking_url(ALT_BASE_OPEN_TRACKING_URL, false, ALT_METADATA);
    auto path = get_open_tracking_url_path(url, ALT_BASE_OPEN_TRACKING_URL);

    auto tracking_result = get_open_tracking_result(path, ALT_WEBHOOK_URL);
    EXPECT_EQ(tracking_result.tracked_url, std::nullopt);
    EXPECT_EQ(tracking_result.webhook_url, ALT_WEBHOOK_URL);
    EXPECT_EQ(tracking_result.request_data, std::nullopt);
    EXPECT_EQ(tracking_result.metadata, ALT_METADATA);
    EXPECT_TRUE(tracking_result.is_open_tracking);
    EXPECT_FALSE(tracking_result.is_click_tracking);
}
TEST(PublicPyTracking, PublicInConfigOpenTrackingUrlToJson) {
    auto url = get_open_tracking_url(ALT_BASE_OPEN_TRACKING_URL, false, ALT_METADATA);
    auto path = get_open_tracking_url_path(url, ALT_BASE_OPEN_TRACKING_URL);

    auto tracking_result = get_open_tracking_result(path, ALT_WEBHOOK_URL);
    auto result_json = tracking_result.to_json_dict();
    EXPECT_EQ(result_json["tracked_url"], nullptr);
    EXPECT_EQ(result_json["webhook_url"], ALT_WEBHOOK_URL);
    EXPECT_EQ(result_json["request_data"], nullptr);
    EXPECT_EQ(result_json["metadata"], ALT_METADATA);
    EXPECT_TRUE(result_json["is_open_tracking"]);
    EXPECT_FALSE(result_json["is_click_tracking"]);
}
TEST(PublicPyTracking, PublicInConfigOpenTrackingFullUrl) {
    auto url = get_open_tracking_url(ALT_BASE_OPEN_TRACKING_URL, false, ALT_METADATA);
    auto tracking_result = get_open_tracking_result(url, ALT_WEBHOOK_URL, ALT_BASE_OPEN_TRACKING_URL);
    EXPECT_EQ(tracking_result.tracked_url, std::nullopt);
    EXPECT_EQ(tracking_result.webhook_url, ALT_WEBHOOK_URL);
    EXPECT_EQ(tracking_result.request_data, std::nullopt);
    EXPECT_EQ(tracking_result.metadata, ALT_METADATA);
    EXPECT_TRUE(tracking_result.is_open_tracking);
    EXPECT_FALSE(tracking_result.is_click_tracking);
}
TEST(PublicPyTracking, PublicEmbeddedOpenTrackingUrl) {
    auto url = get_open_tracking_url(
        ALT_BASE_OPEN_TRACKING_URL, false, ALT_METADATA, ALT_WEBHOOK_URL, true,
        ALT_DEFAULT_METADATA, true
    );
    auto path = get_open_tracking_url_path(url, ALT_BASE_OPEN_TRACKING_URL);

    auto tracking_result = get_open_tracking_result(
        path, ALT_WEBHOOK_URL, std::nullopt, true, true, ALT_REQUEST_DATA
    );

    EXPECT_EQ(tracking_result.tracked_url, std::nullopt);
    EXPECT_EQ(tracking_result.webhook_url, ALT_WEBHOOK_URL);
    EXPECT_EQ(tracking_result.request_data, ALT_REQUEST_DATA);
    EXPECT_EQ(tracking_result.metadata, ALT_EXPECTED_METADATA);
    EXPECT_TRUE(tracking_result.is_open_tracking);
    EXPECT_FALSE(tracking_result.is_click_tracking);
}
TEST(PublicPyTracking, PublicBasicGetClickTrackingUrl) {
    auto url = get_click_tracking_url(ALT_URL_TO_TRACK, ALT_BASE_CLICK_TRACKING_URL);
    EXPECT_TRUE(url.find(ALT_BASE_CLICK_TRACKING_URL) == 0);
    EXPECT_NE(url.find("="), std::string::npos);
}
TEST(PublicPyTracking, PublicBasicGetClickTrackingUrlAppendSlash) {
    auto url = get_click_tracking_url(ALT_URL_TO_TRACK, ALT_BASE_CLICK_TRACKING_URL, true);
    EXPECT_TRUE(url.rfind("/") == (url.length() - 1));
}
TEST(PublicPyTracking, PublicInConfigClickTrackingUrl) {
    auto url = get_click_tracking_url(ALT_URL_TO_TRACK, ALT_BASE_CLICK_TRACKING_URL, false, ALT_METADATA);
    auto path = get_click_tracking_url_path(url, ALT_BASE_CLICK_TRACKING_URL);

    auto tracking_result = get_click_tracking_result(path, ALT_WEBHOOK_URL);
    EXPECT_TRUE(tracking_result.tracked_url.has_value() && tracking_result.tracked_url.value() == ALT_URL_TO_TRACK);
    EXPECT_EQ(tracking_result.webhook_url, ALT_WEBHOOK_URL);
    EXPECT_EQ(tracking_result.request_data, std::nullopt);
    EXPECT_EQ(tracking_result.metadata, ALT_METADATA);
    EXPECT_TRUE(tracking_result.is_click_tracking);
    EXPECT_FALSE(tracking_result.is_open_tracking);
}
TEST(PublicPyTracking, PublicInConfigClickTrackingFullUrl) {
    auto url = get_click_tracking_url(ALT_URL_TO_TRACK, ALT_BASE_CLICK_TRACKING_URL, false, ALT_METADATA);
    auto tracking_result = get_click_tracking_result(url, ALT_WEBHOOK_URL, ALT_BASE_CLICK_TRACKING_URL);

    EXPECT_TRUE(tracking_result.tracked_url.has_value() && tracking_result.tracked_url.value() == ALT_URL_TO_TRACK);
    EXPECT_EQ(tracking_result.webhook_url, ALT_WEBHOOK_URL);
    EXPECT_EQ(tracking_result.request_data, std::nullopt);
    EXPECT_EQ(tracking_result.metadata, ALT_METADATA);
    EXPECT_TRUE(tracking_result.is_click_tracking);
    EXPECT_FALSE(tracking_result.is_open_tracking);
}