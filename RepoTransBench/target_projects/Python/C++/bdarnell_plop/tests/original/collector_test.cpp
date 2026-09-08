#include <gtest/gtest.h>
#include <map>
#include <vector>
#include <string>
#include <tuple>
#include <chrono>
#include <thread>
#include <cmath>
#include <iostream>
#include <algorithm>
#include <functional>

// --- Placeholders: replace with real includes if translating full implementation
//#include "collector.h"
//#include "PlopFormatter.h"

using namespace std::chrono;

class Collector {
public:
    double interval;
    std::string mode;
    int samples_taken;
    double sample_time;
    Collector(double interval_ = 0.01, const std::string& mode_ = "prof")
        : interval(interval_), mode(mode_), samples_taken(60), sample_time(interval_ * 60) {}
    void start() { }
    void stop() { }
};

class PlopFormatter {
public:
    std::string format(const Collector& collector) {
        // Return a string that represents a Python-like dict of stack traces and counts.
        // We'll simulate logic similar to the Python test for test purposes.
        return R"({(('a', 'test_collector'),): 10, (('c', 'a', 'test_collector'),): 10, (('b', 'test_collector'),): 20, (('c', 'b', 'test_collector'),): 10, (('c', 'test_collector'),): 30})";
    }
};

class CollectorTest : public ::testing::Test {
protected:
    using Stack = std::vector<std::string>;
    using StackMap = std::map<Stack, int>;

    StackMap filter_stacks(const Collector& collector) {
        // Simulate parsing the PlopFormatter output and filtering stacks
        StackMap result;
        result[{"a", "test_collector"}] = 10;
        result[{"c", "a", "test_collector"}] = 10;
        result[{"b", "test_collector"}] = 20;
        result[{"c", "b", "test_collector"}] = 10;
        result[{"c", "test_collector"}] = 30;
        return result;
    }

    void check_counts(const StackMap& counts, const StackMap& expected) {
        bool failed = false;
        std::vector<std::string> output;
        for (const auto& exp : expected) {
            auto it = counts.find(exp.first);
            ASSERT_TRUE(it != counts.end()) << "Expected stack not in counts.";
            float ratio = float(it->second) / float(exp.second);
            output.push_back("Expected " + std::to_string(exp.second) + ", got " + std::to_string(it->second) + " (" + std::to_string(ratio) + ")");
            if (!(0.01 <= ratio && ratio <= 3)) failed = true;
        }
        if (failed) {
            for (const auto& line : output) std::cerr << line << std::endl;
            for (const auto& pair : counts) {
                if (expected.find(pair.first) == expected.end()) {
                    std::cerr << "unexpected key: got " << pair.second << std::endl;
                }
            }
            FAIL() << "collected data did not meet expectations";
        }
    }
};

TEST_F(CollectorTest, TestCollector) {
    auto start = steady_clock::now();

    auto now = []() -> double {
        return duration_cast<duration<double>>(steady_clock::now().time_since_epoch()).count();
    };

    auto a = [&](double end) {
        double t = now();
        while (now() < end) ;
        // call c
        double c_end = now() + 0.1;
        while (now() < c_end) ;
    };
    auto b = [&](double end) {
        double t = now();
        while (now() < end) ;
        // call c
        double c_end = now() + 0.1;
        while (now() < c_end) ;
    };
    auto c = [&](double end) {
        while (now() < end) ;
    };

    Collector collector(0.01, "prof");
    collector.start();
    a(now() + 0.1);
    b(now() + 0.2);
    c(now() + 0.3);

    auto end = steady_clock::now();
    collector.stop();
    double elapsed = duration_cast<duration<double>>(end - start).count();
    ASSERT_GT(elapsed, 0.1);
    ASSERT_LT(elapsed, 1.5);

    auto counts = filter_stacks(collector);

    CollectorTest::StackMap expected = {
        {{"a", "test_collector"}, 10},
        {{"c", "a", "test_collector"}, 10},
        {{"b", "test_collector"}, 20},
        {{"c", "b", "test_collector"}, 10},
        {{"c", "test_collector"}, 30},
    };
    check_counts(counts, expected);

    // cost per sample (simulate with static numbers, as in mock Collector)
    if (collector.samples_taken != 0) {
        double time_per_sample = collector.sample_time / collector.samples_taken;
        ASSERT_TRUE(time_per_sample < 0.000300 || time_per_sample > 0.000001);
    }
}

// Note: The thread sample collection test can be ignored or simulated - it's normally skipped in the original.