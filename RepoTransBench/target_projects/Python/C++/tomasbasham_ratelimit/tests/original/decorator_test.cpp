#include <gtest/gtest.h>
#include "ratelimit/decorators.h"
#include "ratelimit/exception.h"

struct ClockMock {
    int t = 0;
    void increment(int dt) { t += dt; }
    int operator()() { return t; }
} clock_mock;

struct DecoratorTest : public ::testing::Test {
    int count;
    void SetUp() override {
        count = 0;
        clock_mock.increment(10);
    }

    int increment() {
        // Allow increment once every 10
        ratelimit::RateLimitDecorator dec(1, 10, std::ref(clock_mock));
        return dec.wrap([this]() { return ++count; })();
    }
    int increment_no_exception() {
        ratelimit::RateLimitDecorator dec(1, 10, std::ref(clock_mock), false);
        return dec.wrap([this]() { return ++count; })();
    }
};

TEST_F(DecoratorTest, Increment) {
    DecoratorTest self;
    self.SetUp();
    self.increment();
    EXPECT_EQ(self.count, 1);
}

TEST_F(DecoratorTest, Exception) {
    DecoratorTest self;
    self.SetUp();
    self.increment();
    EXPECT_THROW(self.increment(), ratelimit::RateLimitException);
}

TEST_F(DecoratorTest, Reset) {
    DecoratorTest self;
    self.SetUp();
    self.increment();
    clock_mock.increment(10);
    self.increment();
    EXPECT_EQ(self.count, 2);
}

TEST_F(DecoratorTest, NoException) {
    DecoratorTest self;
    self.SetUp();
    self.increment_no_exception();
    self.increment_no_exception();
    EXPECT_EQ(self.count, 1); // Only incremented once if rate limited
}