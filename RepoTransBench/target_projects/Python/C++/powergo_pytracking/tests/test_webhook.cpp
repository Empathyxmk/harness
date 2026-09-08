#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include <string>
#include <map>
#include <memory>
#include "pytracking/tracking.h"
#include "pytracking/webhook.h"
#include "pytracking/configuration.h"
#include "util/mock_requests.h" // a mock wrapper for HTTP POST
#include "tests/test_pytracking_utils.h"

using namespace pytracking;
using ::testing::_;
using ::testing::Eq;

TEST(Webhook, SendWebhookClick) {
    std::string url = get_click_tracking_url(
        DEFAULT_URL_TO_TRACK, DEFAULT_BASE_CLICK_TRACKING_URL, false, DEFAULT_METADATA
    );
    std::string path = get_click_tracking_url_path(url, DEFAULT_BASE_CLICK_TRACKING_URL);

    auto tracking_result = get_click_tracking_result(path, DEFAULT_WEBHOOK_URL);

    std::map<std::string, util::Any> payload = {
        {"is_open_tracking", false},
        {"is_click_tracking", true},
        {"metadata", DEFAULT_METADATA},
        {"request_data", nullptr},
        {"tracked_url", DEFAULT_URL_TO_TRACK},
        {"timestamp", tracking_result.timestamp}
    };

    util::MockRequests mock_requests;
    EXPECT_CALL(mock_requests, post(DEFAULT_WEBHOOK_URL, _, Eq(DEFAULT_TIMEOUT_SECONDS)))
        .WillOnce(::testing::Return(true));

    pytracking::webhook::send_webhook(tracking_result, mock_requests);
}

TEST(Webhook, SendWebhookOpen) {
    std::string url = get_open_tracking_url(DEFAULT_BASE_OPEN_TRACKING_URL, false, DEFAULT_METADATA);
    std::string path = get_open_tracking_url_path(url, DEFAULT_BASE_OPEN_TRACKING_URL);

    auto tracking_result = get_open_tracking_result(path, DEFAULT_WEBHOOK_URL);

    std::map<std::string, util::Any> payload = {
        {"is_open_tracking", true},
        {"is_click_tracking", false},
        {"metadata", DEFAULT_METADATA},
        {"request_data", nullptr},
        {"timestamp", tracking_result.timestamp}
    };

    util::MockRequests mock_requests;
    EXPECT_CALL(mock_requests, post(DEFAULT_WEBHOOK_URL, _, Eq(DEFAULT_TIMEOUT_SECONDS)))
        .WillOnce(::testing::Return(true));

    pytracking::webhook::send_webhook(tracking_result, mock_requests);
}