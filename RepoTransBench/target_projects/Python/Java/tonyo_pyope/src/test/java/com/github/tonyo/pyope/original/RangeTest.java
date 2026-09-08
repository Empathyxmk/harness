package com.github.tonyo.pyope.original;

import com.github.tonyo.pyope.errors.InvalidRangeLimitsError;
import com.github.tonyo.pyope.ope.ValueRange;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import static org.junit.jupiter.api.Assertions.*;

import java.util.stream.Stream;

class RangeTest {

    @Test
    void testRangeSimple() {
        long start = 2;
        long end = 1000;
        ValueRange r = new ValueRange(start, end);
        assertEquals(999, r.size());
        for (long i = start; i <= end; i++) {
            assertTrue(r.contains(i));
        }
        assertFalse(r.contains(start - 1));
        assertFalse(r.contains(end + 1));
        assertEquals(10, r.rangeBitSize());
    }

    @Test
    void testRangeRepr() {
        ValueRange a = new ValueRange(1, 10);
        assertEquals(a, ValueRange.fromRepr(a.toString()));
    }

    static Stream<Object[]> invalidRangeEndsProvider() {
        return Stream.of(
                new Object[]{"123", 0},
                new Object[]{0, "123"},
                new Object[]{"123", "abc"}
        );
    }

    @ParameterizedTest
    @MethodSource("invalidRangeEndsProvider")
    void testInvalidRangeEnds(Object start, Object end) {
        assertThrows(InvalidRangeLimitsError.class, () -> {
            new ValueRange(start, end);
        });
    }
}