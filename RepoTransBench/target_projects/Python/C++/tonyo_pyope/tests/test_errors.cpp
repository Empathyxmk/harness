#include <gtest/gtest.h>
#include "errors.h"

TEST(Errors, InvalidCiphertextError) {
    EXPECT_THROW(
        throw InvalidCiphertextError("Cipher error");
    , InvalidCiphertextError);
}

TEST(Errors, InvalidRangeLimitsError) {
    EXPECT_THROW(
        throw InvalidRangeLimitsError("Range error");
    , InvalidRangeLimitsError);
}

TEST(Errors, OutOfRangeError) {
    EXPECT_THROW(
        throw OutOfRangeError("Out of range");
    , OutOfRangeError);
}

TEST(Errors, NotEnoughCoinsError) {
    EXPECT_THROW(
        throw NotEnoughCoinsError("No coins left");
    , NotEnoughCoinsError);
}

TEST(Errors, InvalidCoinError) {
    EXPECT_THROW(
        throw InvalidCoinError("Invalid coin");
    , InvalidCoinError);
}