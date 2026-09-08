#include <gtest/gtest.h>
#include <stdexcept>
#include <string>
#include <chrono>
#include <thread>
#include "../../include/musicbrainzngs.h"
#include "../../include/musicbrainz.h"
#include "../test_helpers/timecop.h"

// Helper for checking if exception message contains a substring
template<typename Func>
void assertThrowsWithMessage(Func&& func, const std::string& substr) {
    bool thrown = false;
    try {
        func();
    } catch (const std::exception& e) {
        thrown = true;
        ASSERT_NE(std::string(e.what()).find(substr), std::string::npos)
            << "Exception message does not contain expected substring: " << substr;
    }
    ASSERT_TRUE(thrown) << "Expected exception not thrown.";
}

// --- RateLimitArgumentTest ---
class RateLimitArgumentTest : public ::testing::Test {};

TEST_F(RateLimitArgumentTest, test_invalid_args) {
    // Invalid limits/intervals should throw ValueError (use std::invalid_argument for C++)
    EXPECT_THROW(
        musicbrainzngs::set_rate_limit(1, 0),
        std::invalid_argument
    );
    try {
        musicbrainzngs::set_rate_limit(1, 0);
        FAIL() << "Required exception wasn't raised";
    } catch (const std::invalid_argument& e) {
        EXPECT_NE(std::string(e.what()).find("new_requests"), std::string::npos);
    }

    EXPECT_THROW(
        musicbrainzngs::set_rate_limit(0, 1),
        std::invalid_argument
    );
    try {
        musicbrainzngs::set_rate_limit(0, 1);
        FAIL() << "Required exception wasn't raised";
    } catch (const std::invalid_argument& e) {
        EXPECT_NE(std::string(e.what()).find("limit_or_interval"), std::string::npos);
    }

    EXPECT_THROW(
        musicbrainzngs::set_rate_limit(1, -1),
        std::invalid_argument
    );
    try {
        musicbrainzngs::set_rate_limit(1, -1);
        FAIL() << "Required exception wasn't raised";
    } catch (const std::invalid_argument& e) {
        EXPECT_NE(std::string(e.what()).find("new_requests"), std::string::npos);
    }

    EXPECT_THROW(
        musicbrainzngs::set_rate_limit(0, -1),
        std::invalid_argument
    );
    try {
        musicbrainzngs::set_rate_limit(0, -1);
        FAIL() << "Required exception wasn't raised";
    } catch (const std::invalid_argument& e) {
        EXPECT_NE(std::string(e.what()).find("limit_or_interval"), std::string::npos);
    }
}

// --- RateLimitingTest ---
class RateLimitingTest : public ::testing::Test {
protected:
    std::unique_ptr<Timecop> cop;
    std::function<void()> func;

    void SetUp() override {
        cop = std::make_unique<Timecop>();
        cop->install();
        // Simulate @musicbrainz._rate_limit
        func = [this] {
            musicbrainz::rate_limited_func();
        };
    }
    void TearDown() override {
        cop->restore();
    }
};

TEST_F(RateLimitingTest, test_do_not_wait_initially) {
    double time1 = Timecop::get_time();
    func();
    double time2 = Timecop::get_time();
    EXPECT_NEAR(time1, time2, 1e-4);
}

TEST_F(RateLimitingTest, test_second_rapid_query_waits) {
    func();
    double time1 = Timecop::get_time();
    func();
    double time2 = Timecop::get_time();
    EXPECT_TRUE(time2 - time1 >= 1.0);
}

TEST_F(RateLimitingTest, test_second_distant_query_does_not_wait) {
    func();
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    double time1 = Timecop::get_time();
    func();
    double time2 = Timecop::get_time();
    EXPECT_NEAR(time1, time2, 1e-4);
}

// --- BatchedRateLimitingTest ---
class BatchedRateLimitingTest : public ::testing::Test {
protected:
    std::unique_ptr<Timecop> cop;
    std::function<void()> func;

    void SetUp() override {
        musicbrainzngs::set_rate_limit(3, 3);
        cop = std::make_unique<Timecop>();
        cop->install();
        func = [this] {
            musicbrainz::rate_limited_func();
        };
    }
    void TearDown() override {
        musicbrainzngs::set_rate_limit(1, 1);
        cop->restore();
    }
};

TEST_F(BatchedRateLimitingTest, test_initial_rapid_queries_not_delayed) {
    double time1 = Timecop::get_time();
    func();
    func();
    func();
    double time2 = Timecop::get_time();
    EXPECT_NEAR(time1, time2, 1e-4);
}

TEST_F(BatchedRateLimitingTest, test_overage_query_delayed) {
    double time1 = Timecop::get_time();
    func();
    func();
    func();
    func();
    double time2 = Timecop::get_time();
    EXPECT_TRUE(time2 - time1 >= 1.0);
}

// --- NoRateLimitingTest ---
class NoRateLimitingTest : public ::testing::Test {
protected:
    std::unique_ptr<Timecop> cop;
    std::function<void()> func;

    void SetUp() override {
        musicbrainzngs::set_rate_limit(false);
        cop = std::make_unique<Timecop>();
        cop->install();
        func = [this] {
            musicbrainz::rate_limited_func();
        };
    }
    void TearDown() override {
        musicbrainzngs::set_rate_limit(true);
        cop->restore();
    }
};

TEST_F(NoRateLimitingTest, test_initial_rapid_queries_not_delayed) {
    double time1 = Timecop::get_time();
    func();
    func();
    func();
    double time2 = Timecop::get_time();
    EXPECT_NEAR(time1, time2, 1e-4);
}