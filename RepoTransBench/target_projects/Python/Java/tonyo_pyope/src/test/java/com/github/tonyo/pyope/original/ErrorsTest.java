package com.github.tonyo.pyope.original;

import com.github.tonyo.pyope.errors.*;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class ErrorsTest {

    @Test
    void testInvalidCiphertextError() {
        assertThrows(InvalidCiphertextError.class, () -> {
            throw new InvalidCiphertextError("Cipher error");
        });
    }

    @Test
    void testInvalidRangeLimitsError() {
        assertThrows(InvalidRangeLimitsError.class, () -> {
            throw new InvalidRangeLimitsError("Range error");
        });
    }

    @Test
    void testOutOfRangeError() {
        assertThrows(OutOfRangeError.class, () -> {
            throw new OutOfRangeError("Out of range");
        });
    }

    @Test
    void testNotEnoughCoinsError() {
        assertThrows(NotEnoughCoinsError.class, () -> {
            throw new NotEnoughCoinsError("No coins left");
        });
    }

    @Test
    void testInvalidCoinError() {
        assertThrows(InvalidCoinError.class, () -> {
            throw new InvalidCoinError("Invalid coin");
        });
    }
}