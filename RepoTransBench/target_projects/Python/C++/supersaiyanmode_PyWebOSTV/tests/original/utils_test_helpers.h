#ifndef UTILS_TEST_HELPERS_H
#define UTILS_TEST_HELPERS_H

#include <gtest/gtest.h>
#include <queue>
#include <mutex>
#include <condition_variable>
#include <thread>
#include <unordered_map>
#include <string>
#include <vector>
#include <set>
#include <map>
#include <stdexcept>
#include <atomic>
#include <functional>

// -------- FakeClient and helpers --------

// Fake queue (for simulating blocking queue operations)
template<typename T>
class BlockingQueue {
public:
    void put(const T& item) {
        std::unique_lock<std::mutex> lock(mtx);
        queue.push(item);
        cv.notify_all();
    }
    T get(bool block = true, int timeout_ms = 1000) {
        std::unique_lock<std::mutex> lock(mtx);
        if(block) {
            if(!cv.wait_for(lock, std::chrono::milliseconds(timeout_ms), [this]{ return !queue.empty(); })) {
                throw std::runtime_error("Queue timeout");
            }
        }
        if(queue.empty()) throw std::runtime_error("Queue empty");
        T item = queue.front();
        queue.pop();
        return item;
    }
private:
    std::queue<T> queue;
    std::mutex mtx;
    std::condition_variable cv;
};

// Helper fake dictionary class (rough equivalent for python's dict for small tests)
class FakeDict {
public:
    FakeDict() {}
    FakeDict(std::initializer_list<std::pair<std::string, std::string>> items) {
        for(const auto& kv : items) data[kv.first] = kv.second;
    }
    std::string& operator[](const std::string& k) { return data[k]; }
    const std::string& at(const std::string& k) const { return data.at(k); }
    bool contains(const std::string& k) const { return data.count(k) != 0; }
    bool operator==(const FakeDict& o) const { return data == o.data; }
    std::map<std::string, std::string> data;
};

// FakeClient mimics the pywebostv "client" for test verification
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
        sent_message["payload"] = "[payload]"; // placeholder
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
        // For simplicity, just store the mapping
        pending_responses[uri] = response;
    }
    void received_message(const std::string& json_msg) {
        // No-op, can parse for more complete simulation
        received_queue.put(json_msg);
    }
    std::map<std::string, std::string> sent_message;
    std::map<std::string, std::map<std::string, std::string>> pending_responses;
    int sent_message_count;
    BlockingQueue<std::string> received_queue;
private:
    std::mutex _mutex;
};

#endif // UTILS_TEST_HELPERS_H