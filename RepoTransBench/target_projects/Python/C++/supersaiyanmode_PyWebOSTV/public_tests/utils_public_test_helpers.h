#ifndef UTILS_PUBLIC_TEST_HELPERS_H
#define UTILS_PUBLIC_TEST_HELPERS_H

#include <gtest/gtest.h>
#include <queue>
#include <string>
#include <map>
#include <mutex>

// Same as utils_test_helpers, but for public tests (makes separation simple)
class FakeClient {
public:
    explicit FakeClient() : sent_message_count(0) {}

    void send_message(const std::string& type, const std::string& uri,
                      const std::map<std::string, std::string>& payload,
                      const std::string& unique_id = "",
                      bool /*get_queue*/ = false
                      ) {
        std::lock_guard<std::mutex> lock(_mutex);
        sent_message.clear();
        sent_message["type"] = type;
        sent_message["uri"] = uri;
        sent_message["payload"] = "[payload]";
        if (!unique_id.empty()) sent_message["id"] = unique_id;
        sent_message_count++;
    }
    void send_message(const std::string& type, const std::string& uri,
                      std::nullptr_t,
                      const std::string& unique_id = "",
                      bool /*get_queue*/ = false) {
        std::lock_guard<std::mutex> lock(_mutex);
        sent_message.clear();
        sent_message["type"] = type;
        sent_message["uri"] = uri;
        if (!unique_id.empty()) sent_message["id"] = unique_id;
        sent_message_count++;
    }
    void assert_sent_message(const std::map<std::string, std::string>& expected) {
        for (const auto& kv : expected) {
            ASSERT_TRUE(sent_message.count(kv.first)) << "Key missing: " << kv.first;
            EXPECT_EQ(sent_message.at(kv.first), kv.second);
        }
    }
    void assert_sent_message_without_id(const std::map<std::string, std::string>& expected) {
        for (const auto& kv : expected) {
            if(kv.first == "id") continue;
            ASSERT_TRUE(sent_message.count(kv.first)) << "Key missing: " << kv.first;
            EXPECT_EQ(sent_message.at(kv.first), kv.second);
        }
    }
    void setup_response(const std::string& uri, const std::map<std::string, std::string>& response) {
        pending_responses[uri] = response;
    }
    std::map<std::string, std::string> sent_message;
    std::map<std::string, std::map<std::string, std::string>> pending_responses;
    int sent_message_count;
private:
    std::mutex _mutex;
};

#endif // UTILS_PUBLIC_TEST_HELPERS_H