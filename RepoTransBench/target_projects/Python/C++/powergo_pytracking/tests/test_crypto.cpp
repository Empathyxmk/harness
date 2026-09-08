#include <gtest/gtest.h>
#include <string>
#include <map>
#include <memory>
#include "pytracking/configuration.h"
#include "pytracking/tracking.h"
#include "util/crypto.h" // assume fernet support

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

#ifdef HAS_CRYPTOGRAPHY
TEST(Crypto, BasicEncryptedGetOpenTrackingUrl) {
    auto url = get_open_tracking_url(DEFAULT_BASE_OPEN_TRACKING_URL, false, {}, "", false, {}, false, DEFAULT_ENCRYPTION_KEY);
    auto path = get_open_tracking_url_path(url, DEFAULT_BASE_OPEN_TRACKING_URL);
    auto key = util::fernet_from_key(DEFAULT_ENCRYPTION_KEY);
    auto value = key.decrypt(path);
    ASSERT_FALSE(value.empty());
}
#endif

#ifdef HAS_CRYPTOGRAPHY
TEST(Crypto, MinimalEncryptedGetOpenTrackingUrl) {
    auto url = get_open_tracking_url(
        DEFAULT_BASE_OPEN_TRACKING_URL, false, DEFAULT_METADATA, "", false,
        {}, false, DEFAULT_ENCRYPTION_KEY
    );
    auto path = get_open_tracking_url_path(url, DEFAULT_BASE_OPEN_TRACKING_URL);

    auto tracking_result = get_open_tracking_result(
        path,
        DEFAULT_WEBHOOK_URL,
        DEFAULT_DEFAULT_METADATA,
        true,
        true,
        DEFAULT_REQUEST_DATA,
        DEFAULT_ENCRYPTION_KEY
    );

    auto expected_metadata = DEFAULT_DEFAULT_METADATA;
    expected_metadata.insert(DEFAULT_METADATA.begin(), DEFAULT_METADATA.end());

    EXPECT_EQ(tracking_result.tracked_url, std::nullopt);
    EXPECT_EQ(tracking_result.webhook_url, DEFAULT_WEBHOOK_URL);
    EXPECT_EQ(tracking_result.request_data, DEFAULT_REQUEST_DATA);
    EXPECT_EQ(tracking_result.metadata, expected_metadata);
    EXPECT_TRUE(tracking_result.is_open_tracking);
    EXPECT_FALSE(tracking_result.is_click_tracking);
}
#endif

#ifdef HAS_CRYPTOGRAPHY
TEST(Crypto, BasicEncryptedGetClickTrackingUrl) {
    auto url = get_click_tracking_url(DEFAULT_URL_TO_TRACK, DEFAULT_BASE_CLICK_TRACKING_URL, false, {}, "", false, {}, false, DEFAULT_ENCRYPTION_KEY);
    auto path = get_click_tracking_url_path(url, DEFAULT_BASE_CLICK_TRACKING_URL);
    auto key = util::fernet_from_key(DEFAULT_ENCRYPTION_KEY);
    auto value = key.decrypt(path);
    ASSERT_FALSE(value.empty());
}
#endif

#ifdef HAS_CRYPTOGRAPHY
TEST(Crypto, MinimalEncryptedGetClickTrackingUrl) {
    auto url = get_click_tracking_url(DEFAULT_URL_TO_TRACK, DEFAULT_BASE_CLICK_TRACKING_URL, false, DEFAULT_METADATA, "", false, {}, false, DEFAULT_ENCRYPTION_KEY);
    auto path = get_click_tracking_url_path(url, DEFAULT_BASE_CLICK_TRACKING_URL);

    auto tracking_result = get_click_tracking_result(
        path,
        DEFAULT_WEBHOOK_URL,
        DEFAULT_DEFAULT_METADATA,
        true,
        true,
        DEFAULT_REQUEST_DATA,
        DEFAULT_ENCRYPTION_KEY
    );

    auto expected_metadata = DEFAULT_DEFAULT_METADATA;
    expected_metadata.insert(DEFAULT_METADATA.begin(), DEFAULT_METADATA.end());

    EXPECT_EQ(tracking_result.tracked_url.value(), DEFAULT_URL_TO_TRACK);
    EXPECT_EQ(tracking_result.webhook_url, DEFAULT_WEBHOOK_URL);
    EXPECT_EQ(tracking_result.request_data, DEFAULT_REQUEST_DATA);
    EXPECT_EQ(tracking_result.metadata, expected_metadata);
    EXPECT_TRUE(tracking_result.is_click_tracking);
    EXPECT_FALSE(tracking_result.is_open_tracking);
}
#endif