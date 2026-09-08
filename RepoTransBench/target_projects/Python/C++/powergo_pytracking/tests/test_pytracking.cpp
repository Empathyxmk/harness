#include <gtest/gtest.h>
#include <string>
#include <map>
#include <memory>
#include "pytracking/configuration.h"
#include "pytracking/tracking.h"
// Assume appropriate util functions for json, etc.

using namespace pytracking;

const std::string DEFAULT_URL_TO_TRACK = "https://www.bob.com/hello-world/?token=valueééé";
const std::string DEFAULT_BASE_CLICK_TRACKING_URL = "https://a.b.com/tracking/";
const std::string DEFAULT_BASE_OPEN_TRACKING_URL = "https://a.b.com/tracking/open/";
const std::string DEFAULT_WEBHOOK_URL = "https://webhook.com/tracking/";

std::map<std::string, util::Any> DEFAULT_METADATA = {
    {"param1", "val1"},
    {"param3", "val3b"},
    {"nested", std::map<std::string, util::Any>{{"param2", "val2"}}}
};

std::map<std::string, util::Any> DEFAULT_DEFAULT_METADATA = {
    {"key1", true},
    {"keyéé", "valèèè"},
    {"param3", "val3"}
};
std::map<std::string, util::Any> EXPECTED_METADATA = []{
    auto em = DEFAULT_DEFAULT_METADATA;
    em.insert(DEFAULT_METADATA.begin(), DEFAULT_METADATA.end());
    return em;
}();
std::map<std::string, util::Any> DEFAULT_REQUEST_DATA = {
    {"user_agent", "Firefox"},
    {"user_ip", "127.0.0.1"}
};

Configuration DEFAULT_CONFIGURATION(
    DEFAULT_WEBHOOK_URL,
    DEFAULT_BASE_OPEN_TRACKING_URL,
    DEFAULT_BASE_CLICK_TRACKING_URL,
    DEFAULT_DEFAULT_METADATA
);

TEST(PyTracking, GetOpenTrackingPixel) {
    auto [pixel, mime] = get_open_tracking_pixel();
    EXPECT_EQ(pixel.size(), 68);
    EXPECT_EQ(mime, "image/png");
}

TEST(PyTracking, BasicGetOpenTrackingUrl) {
    auto url = get_open_tracking_url(DEFAULT_BASE_OPEN_TRACKING_URL);
    EXPECT_EQ(url, "https://a.b.com/tracking/open/e30=");
}

TEST(PyTracking, BasicGetOpenTrackingUrlAppendSlash) {
    auto url = get_open_tracking_url(DEFAULT_BASE_OPEN_TRACKING_URL, true);
    EXPECT_EQ(url, "https://a.b.com/tracking/open/e30=/");
}

TEST(PyTracking, InConfigOpenTrackingUrl) {
    auto url = get_open_tracking_url(DEFAULT_BASE_OPEN_TRACKING_URL, false, DEFAULT_METADATA);
    auto path = get_open_tracking_url_path(url, DEFAULT_BASE_OPEN_TRACKING_URL);

    auto tracking_result = get_open_tracking_result(path, DEFAULT_WEBHOOK_URL);
    EXPECT_EQ(tracking_result.tracked_url, std::nullopt);
    EXPECT_EQ(tracking_result.webhook_url, DEFAULT_WEBHOOK_URL);
    EXPECT_EQ(tracking_result.request_data, std::nullopt);
    EXPECT_EQ(tracking_result.metadata, DEFAULT_METADATA);
    EXPECT_EQ(tracking_result.is_open_tracking, true);
    EXPECT_EQ(tracking_result.is_click_tracking, false);
}

TEST(PyTracking, InConfigOpenTrackingUrlToJson) {
    auto url = get_open_tracking_url(DEFAULT_BASE_OPEN_TRACKING_URL, false, DEFAULT_METADATA);
    auto path = get_open_tracking_url_path(url, DEFAULT_BASE_OPEN_TRACKING_URL);
    auto tracking_result = get_open_tracking_result(path, DEFAULT_WEBHOOK_URL);
    auto result_json = tracking_result.to_json_dict();
    EXPECT_EQ(result_json["tracked_url"], nullptr);
    EXPECT_EQ(result_json["webhook_url"], DEFAULT_WEBHOOK_URL);
    EXPECT_EQ(result_json["request_data"], nullptr);
    EXPECT_EQ(result_json["metadata"], DEFAULT_METADATA);
    EXPECT_EQ(result_json["is_open_tracking"], true);
    EXPECT_EQ(result_json["is_click_tracking"], false);
}

TEST(PyTracking, InConfigOpenTrackingFullUrl) {
    auto url = get_open_tracking_url(DEFAULT_BASE_OPEN_TRACKING_URL, false, DEFAULT_METADATA);
    auto tracking_result = get_open_tracking_result(url, DEFAULT_WEBHOOK_URL, DEFAULT_BASE_OPEN_TRACKING_URL);
    EXPECT_EQ(tracking_result.tracked_url, std::nullopt);
    EXPECT_EQ(tracking_result.webhook_url, DEFAULT_WEBHOOK_URL);
    EXPECT_EQ(tracking_result.request_data, std::nullopt);
    EXPECT_EQ(tracking_result.metadata, DEFAULT_METADATA);
    EXPECT_EQ(tracking_result.is_open_tracking, true);
    EXPECT_EQ(tracking_result.is_click_tracking, false);
}

TEST(PyTracking, EmbeddedOpenTrackingUrl) {
    auto url = get_open_tracking_url(
        DEFAULT_BASE_OPEN_TRACKING_URL, false, DEFAULT_METADATA, DEFAULT_WEBHOOK_URL, true,
        DEFAULT_DEFAULT_METADATA, true
    );
    auto path = get_open_tracking_url_path(url, DEFAULT_BASE_OPEN_TRACKING_URL);

    auto tracking_result = get_open_tracking_result(
        path, DEFAULT_WEBHOOK_URL, std::nullopt, true, true, DEFAULT_REQUEST_DATA
    );
    EXPECT_EQ(tracking_result.tracked_url, std::nullopt);
    EXPECT_EQ(tracking_result.webhook_url, DEFAULT_WEBHOOK_URL);
    EXPECT_EQ(tracking_result.request_data, DEFAULT_REQUEST_DATA);
    EXPECT_EQ(tracking_result.metadata, EXPECTED_METADATA);
    EXPECT_EQ(tracking_result.is_open_tracking, true);
    EXPECT_EQ(tracking_result.is_click_tracking, false);
}

TEST(PyTracking, BasicGetClickTrackingUrl) {
    auto url = get_click_tracking_url(DEFAULT_URL_TO_TRACK, DEFAULT_BASE_CLICK_TRACKING_URL);
    EXPECT_EQ(url, "https://a.b.com/tracking/eyJ1cmwiOiAiaHR0cHM6Ly93d3cuYm9iLmNvbS9oZWxsby13b3JsZC8_dG9rZW49dmFsdWVcdTAwZTlcdTAwZTlcdTAwZTkifQ==");
}
TEST(PyTracking, BasicGetClickTrackingUrlAppendSlash) {
    auto url = get_click_tracking_url(DEFAULT_URL_TO_TRACK, DEFAULT_BASE_CLICK_TRACKING_URL, true);
    EXPECT_EQ(url, "https://a.b.com/tracking/eyJ1cmwiOiAiaHR0cHM6Ly93d3cuYm9iLmNvbS9oZWxsby13b3JsZC8_dG9rZW49dmFsdWVcdTAwZTlcdTAwZTlcdTAwZTkifQ==/");
}

TEST(PyTracking, InConfigClickTrackingUrl) {
    auto url = get_click_tracking_url(DEFAULT_URL_TO_TRACK, DEFAULT_BASE_CLICK_TRACKING_URL, false, DEFAULT_METADATA);
    auto path = get_click_tracking_url_path(url, DEFAULT_BASE_CLICK_TRACKING_URL);

    auto tracking_result = get_click_tracking_result(path, DEFAULT_WEBHOOK_URL);
    EXPECT_EQ(tracking_result.tracked_url.value(), DEFAULT_URL_TO_TRACK);
    EXPECT_EQ(tracking_result.webhook_url, DEFAULT_WEBHOOK_URL);
    EXPECT_EQ(tracking_result.request_data, std::nullopt);
    EXPECT_EQ(tracking_result.metadata, DEFAULT_METADATA);
    EXPECT_EQ(tracking_result.is_click_tracking, true);
    EXPECT_EQ(tracking_result.is_open_tracking, false);
}

TEST(PyTracking, InConfigClickTrackingFullUrl) {
    auto url = get_click_tracking_url(DEFAULT_URL_TO_TRACK, DEFAULT_BASE_CLICK_TRACKING_URL, false, DEFAULT_METADATA);

    auto tracking_result = get_click_tracking_result(
        url, DEFAULT_WEBHOOK_URL, DEFAULT_BASE_CLICK_TRACKING_URL
    );
    EXPECT_EQ(tracking_result.tracked_url.value(), DEFAULT_URL_TO_TRACK);
    EXPECT_EQ(tracking_result.webhook_url, DEFAULT_WEBHOOK_URL);
    EXPECT_EQ(tracking_result.request_data, std::nullopt);
    EXPECT_EQ(tracking_result.metadata, DEFAULT_METADATA);
    EXPECT_EQ(tracking_result.is_click_tracking, true);
    EXPECT_EQ(tracking_result.is_open_tracking, false);
}

TEST(PyTracking, EmbeddedClickTrackingUrl) {
    auto url = get_click_tracking_url(
        DEFAULT_URL_TO_TRACK,
        DEFAULT_BASE_CLICK_TRACKING_URL,
        false,
        DEFAULT_METADATA,
        DEFAULT_WEBHOOK_URL,
        true,
        DEFAULT_DEFAULT_METADATA,
        true
    );
    auto path = get_click_tracking_url_path(url, DEFAULT_BASE_CLICK_TRACKING_URL);

    auto tracking_result = get_click_tracking_result(
        path, DEFAULT_WEBHOOK_URL, std::nullopt, true, true, DEFAULT_REQUEST_DATA
    );
    EXPECT_EQ(tracking_result.tracked_url.value(), DEFAULT_URL_TO_TRACK);
    EXPECT_EQ(tracking_result.webhook_url, DEFAULT_WEBHOOK_URL);
    EXPECT_EQ(tracking_result.request_data, DEFAULT_REQUEST_DATA);
    EXPECT_EQ(tracking_result.metadata, EXPECTED_METADATA);
    EXPECT_EQ(tracking_result.is_click_tracking, true);
    EXPECT_EQ(tracking_result.is_open_tracking, false);
}