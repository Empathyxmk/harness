#include <gtest/gtest.h>
#include "src/ai_models/stepper.h"
#include <sstream>
#include <memory>

// A helper to capture log outputs (simulating caplog in Python)
class LogCapture {
    std::stringstream buffer;
    std::streambuf* old;
public:
    LogCapture() : old(std::clog.rdbuf(buffer.rdbuf())) {}
    ~LogCapture() { std::clog.rdbuf(old); }
    std::string str() { return buffer.str(); }
};

TEST(StepperTests, StepperBasic) {
    LogCapture log_capture;
    Stepper s(2, 6);
    ASSERT_EQ(s.num_steps(), 3);
    s.begin();
    s.step(0, 2);
    s.step(1, 2);
    s.step(2, 2);
    s.end();
    std::string logs = log_capture.str();
    EXPECT_NE(logs.find("Elapsed"), std::string::npos);
    EXPECT_NE(logs.find("Average"), std::string::npos);
}

TEST(StepperTests, StepperZeroSteps) {
    LogCapture log_capture;
    Stepper s(5, 0);
    s.begin();
    s.end();
    std::string logs = log_capture.str();
    // No assertion on "Average" since 0 steps; could check not present but generally just ensure no crash
    SUCCEED();
}