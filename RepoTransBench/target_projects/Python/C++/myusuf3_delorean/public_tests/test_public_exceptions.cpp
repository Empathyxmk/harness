#include <gtest/gtest.h>
#include "delorean_stub.h"

using namespace delorean;

TEST(PublicDeloreanExceptions, ErrorStrPublic) {
    DeloreanError e("public error!");
    EXPECT_STREQ(e.what(), "public error!");
    EXPECT_TRUE(dynamic_cast<std::exception*>(&e) != nullptr);
}

TEST(PublicDeloreanExceptions, InvalidTimezoneIsSubclassPublic) {
    DeloreanInvalidTimezone e("public bad tz");
    EXPECT_STREQ(e.what(), "public bad tz");
    EXPECT_TRUE(dynamic_cast<DeloreanError*>(&e) != nullptr);
}

TEST(PublicDeloreanExceptions, InvalidDatetimeIsSubclassPublic) {
    DeloreanInvalidDatetime e("public bad dt");
    EXPECT_STREQ(e.what(), "public bad dt");
    EXPECT_TRUE(dynamic_cast<DeloreanError*>(&e) != nullptr);
}