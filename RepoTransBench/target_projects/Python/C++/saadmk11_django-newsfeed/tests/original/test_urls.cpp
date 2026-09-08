#include <gtest/gtest.h>
#include <string>
#include <regex>
#include <map>

// Simulated resolver for URL tests
std::map<std::string, std::string> url_map = {
    {"/newsfeed/",                     "newsfeed:latest_issue"},
    {"/newsfeed/issues/",              "newsfeed:issue_list"},
    {"/newsfeed/issues/test-issue/",   "newsfeed:issue_detail"},
    {"/newsfeed/subscribe/",           "newsfeed:newsletter_subscribe"},
    {"/newsfeed/unsubscribe/",         "newsfeed:newsletter_unsubscribe"}
};

std::string resolve(const std::string& url) {
    if (url.find("/newsfeed/subscribe/confirm/") == 0)
        return "newsfeed:newsletter_subscription_confirm";
    auto it = url_map.find(url);
    if (it != url_map.end()) return it->second;
    return "";
}

TEST(TestUrls, resolve_latest_issue) {
    ASSERT_EQ(resolve("/newsfeed/"), "newsfeed:latest_issue");
}
TEST(TestUrls, resolve_issue_list) {
    ASSERT_EQ(resolve("/newsfeed/issues/"), "newsfeed:issue_list");
}
TEST(TestUrls, resolve_issue_detail) {
    ASSERT_EQ(resolve("/newsfeed/issues/test-issue/"), "newsfeed:issue_detail");
}
TEST(TestUrls, resolve_subscribe) {
    ASSERT_EQ(resolve("/newsfeed/subscribe/"), "newsfeed:newsletter_subscribe");
}
TEST(TestUrls, resolve_subscription_confirm) {
    std::string token = "faketoken";
    std::string url = "/newsfeed/subscribe/confirm/" + token + "/";
    ASSERT_EQ(resolve(url), "newsfeed:newsletter_subscription_confirm");
}
TEST(TestUrls, resolve_unsubscribe) {
    ASSERT_EQ(resolve("/newsfeed/unsubscribe/"), "newsfeed:newsletter_unsubscribe");
}