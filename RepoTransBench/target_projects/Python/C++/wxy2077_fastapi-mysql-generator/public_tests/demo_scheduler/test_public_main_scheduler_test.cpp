#include <gtest/gtest.h>
#include <vector>
#include <chrono>
#include <set>

using namespace std;
using namespace std::chrono;

std::vector<system_clock::time_point> next_time(system_clock::time_point start, seconds delta, int count) {
    std::vector<system_clock::time_point> times;
    auto t = start;
    for (int i = 0; i < count; ++i) {
        t += delta;
        times.push_back(t);
    }
    return times;
}

TEST(PublicDemoSchedulerTest, PublicScheduleAddition) {
    // Start: 2025-07-01 10:00:00 UTC
    tm start_tm = {};
    start_tm.tm_year = 2025 - 1900;
    start_tm.tm_mon = 6;
    start_tm.tm_mday = 1;
    start_tm.tm_hour = 10;
    auto start = system_clock::from_time_t(timegm(&start_tm));
    auto delta = seconds(20);

    auto times = next_time(start, delta, 2);
    ASSERT_EQ(times.size(), 2);
    ASSERT_GT(times[0], start);
    auto diff = duration_cast<seconds>(times[1] - times[0]).count();
    ASSERT_EQ(diff, 20);
}

TEST(PublicDemoSchedulerTest, PublicScheduleTimesUnique) {
    tm start_tm = {};
    start_tm.tm_year = 2024 - 1900;
    start_tm.tm_mon = 11; // December (0-based)
    start_tm.tm_mday = 31;
    start_tm.tm_hour = 23;
    start_tm.tm_min = 45;
    auto start = system_clock::from_time_t(timegm(&start_tm));
    auto delta = minutes(3);
    std::vector<system_clock::time_point> times;
    for (int i = 0; i < 4; ++i) {
        times.push_back(start + delta * i);
    }
    std::set<system_clock::time_point> unique_times(times.begin(), times.end());
    ASSERT_EQ(unique_times.size(), 4);
    ASSERT_GT(times.back(), start);
}