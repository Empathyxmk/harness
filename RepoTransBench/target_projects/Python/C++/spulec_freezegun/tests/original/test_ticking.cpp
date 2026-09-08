#include <gtest/gtest.h>
#include <chrono>
#include <thread>

TEST(Ticking, TickingDatetime) {
    // Simulate ticking time: time progresses after sleeping
    auto start = std::chrono::system_clock::now();
    std::this_thread::sleep_for(std::chrono::milliseconds(1));
    auto end = std::chrono::system_clock::now();
    ASSERT_GT(end, start);
}

TEST(Ticking, TickingTime) {
    // Simulate time.time() + sleep: time/time_after > time_before
    auto before = std::chrono::system_clock::now();
    std::this_thread::sleep_for(std::chrono::milliseconds(2));
    auto after = std::chrono::system_clock::now();
    ASSERT_GT(after, before);
}