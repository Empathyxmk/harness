#include <gtest/gtest.h>
#include "delorean_stub.h"
#include <stdexcept>
#include <string>

using namespace delorean;

TEST(DeloreanExceptionsTest, DeloreanErrorStr) {
    DeloreanError e("msg!");
    EXPECT_STREQ(e.what(), "msg!");
    EXPECT_TRUE(dynamic_cast<std::exception*>(&e) != nullptr);
}

TEST(DeloreanExceptionsTest, InvalidTimezoneIsSubclass) {
    DeloreanInvalidTimezone e("bad tz");
    EXPECT_STREQ(e.what(), "bad tz");
    EXPECT_TRUE(dynamic_cast<DeloreanError*>(&e) != nullptr);
}

TEST(DeloreanExceptionsTest, InvalidDatetimeIsSubclass) {
    DeloreanInvalidDatetime e("bad dt");
    EXPECT_STREQ(e.what(), "bad dt");
    EXPECT_TRUE(dynamic_cast<DeloreanError*>(&e) != nullptr);
}