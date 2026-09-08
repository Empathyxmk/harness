#include <gtest/gtest.h>
#include <thread>
#include <chrono>
#include <future>

TEST(AsyncioTest, AsyncAdd) {
    auto add = [](int a, int b) {
        std::this_thread::sleep_for(std::chrono::milliseconds(1));
        return a + b;
    };
    auto fut = std::async(std::launch::async, add, 14, 7);
    ASSERT_EQ(fut.get(), 21);
}

TEST(AsyncioTest, AsyncUpper) {
    auto upper = [](const std::string& s) {
        std::this_thread::sleep_for(std::chrono::milliseconds(1));
        std::string u = s;
        for (auto& c : u) c = ::toupper(c);
        return u;
    };
    auto fut = std::async(std::launch::async, upper, std::string("publictest"));
    ASSERT_EQ(fut.get(), "PUBLICTEST");
}