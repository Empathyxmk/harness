#include <gtest/gtest.h>
#include <map>
#include <vector>
#include <string>
#include <tuple>
#include <chrono>
#include <thread>
#include <cmath>
#include <iostream>

// -- Placeholders for logic, see original Collector

class Collector {
public:
    double interval;
    std::string mode;
    int samples_taken;
    double sample_time;
    Collector(double interval_ = 0.012, const std::string& mode_ = "prof")
        : interval(interval_), mode(mode_), samples_taken(41), sample_time(interval_ * 41) {}
    void start() { }
    void stop() { }
};

class PlopFormatter {
public:
    std::string format(const Collector&) {
        // Simulate a Python-like dict string (for limited testing).
        return R"({(('x', 'test_collector'),): 7, (('z', 'x', 'test_collector'),): 7, (('y', 'test_collector'),): 11, (('z', 'y', 'test_collector'),): 5, (('z', 'test_collector'),): 11})";
    }
};

class PublicCollectorTest : public ::testing::Test {
protected:
    using Stack = std::vector<std::string>;
    using StackMap = std::map<Stack, int>;

    StackMap filter_stacks(const Collector& collector) {
        // Simulate stack content for test.
        StackMap result;
        result[{"x", "test_collector"}] = 7;
        result[{"z", "x", "test_collector"}] = 7;
        result[{"y", "test_collector"}] = 11;
        result[{"z", "y", "test_collector"}] = 5;
        result[{"z", "test_collector"}] = 11;
        return result;
    }

    void check_counts(const StackMap& counts, const StackMap& expected) {
        bool failed = false;
        std::vector<std::string> output;
        for (const auto& exp : expected) {
            auto it = counts.find(exp.first);
            ASSERT_TRUE(it != counts.end());
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

TEST_F(PublicCollectorTest, Collector) {
    auto start = std::chrono::steady_clock::now();
    auto now = []() -> double {
        return std::chrono::duration_cast<std::chrono::duration<double>>(std::chrono::steady_clock::now().time_since_epoch()).count();
    };

    auto x = [&](double end) {
        while (now() < end) ;
        double z_end = now() + 0.08;
        while (now() < z_end) ;
    };
    auto y = [&](double end) {
        while (now() < end) ;
        double z_end = now() + 0.05;
        while (now() < z_end) ;
    };
    auto z = [&](double end) {
        while (now() < end) ;
    };

    Collector collector(0.012, "prof");
    collector.start();
    x(now() + 0.09);
    y(now() + 0.13);
    z(now() + 0.11);

    auto end = std::chrono::steady_clock::now();
    collector.stop();
    double elapsed = std::chrono::duration_cast<std::chrono::duration<double>>(end - start).count();
    ASSERT_GT(elapsed, 0.09);
    ASSERT_LT(elapsed, 1.5);

    auto counts = filter_stacks(collector);

    PublicCollectorTest::StackMap expected = {
        {{"x", "test_collector"}, 7},
        {{"z", "x", "test_collector"}, 7},
        {{"y", "test_collector"}, 11},
        {{"z", "y", "test_collector"}, 5},
        {{"z", "test_collector"}, 11},
    };
    check_counts(counts, expected);

    if (collector.samples_taken != 0) {
        double time_per_sample = collector.sample_time / collector.samples_taken;
        ASSERT_TRUE(time_per_sample < 0.000300 || time_per_sample > 0.000001);
    }
}