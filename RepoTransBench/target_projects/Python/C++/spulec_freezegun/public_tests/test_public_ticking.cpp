#include <gtest/gtest.h>
#include <chrono>
#include <thread>

TEST(PublicTickingTest, TimeProgression) {
    auto t1 = std::chrono::system_clock::now();
    std::this_thread::sleep_for(std::chrono::milliseconds(2));
    auto t2 = std::chrono::system_clock::now();
    EXPECT_GT(t2, t1);
}

TEST(PublicTickingTest, PerfCounterProgression) {
    auto c1 = std::chrono::high_resolution_clock::now();
    std::this_thread::sleep_for(std::chrono::milliseconds(3));
    auto c2 = std::chrono::high_resolution_clock::now();
    EXPECT_GT(c2, c1);
}