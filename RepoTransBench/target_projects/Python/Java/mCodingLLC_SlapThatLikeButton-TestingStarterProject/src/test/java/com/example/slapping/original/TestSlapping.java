package com.example.slapping.original;

import com.example.slapping.*;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import static org.junit.jupiter.api.Assertions.*;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.util.stream.Stream;

/**
 * Ported from tests/test_slapping.py
 */
class TestSlapping {

    @Test
    void testEmptySlap() {
        assertSame(LikeState.EMPTY, SlapThatLikeButton.slapMany(LikeState.EMPTY, ""));
    }

    @Test
    void testSingleSlaps() {
        assertSame(LikeState.LIKED, SlapThatLikeButton.slapMany(LikeState.EMPTY, "l"));
        assertSame(LikeState.DISLIKED, SlapThatLikeButton.slapMany(LikeState.EMPTY, "d"));
    }

    static Stream<org.junit.jupiter.params.provider.Arguments> provideMultiSlaps() {
        return Stream.of(
                org.junit.jupiter.params.provider.Arguments.of("ll", LikeState.EMPTY),
                org.junit.jupiter.params.provider.Arguments.of("dd", LikeState.EMPTY),
                org.junit.jupiter.params.provider.Arguments.of("ld", LikeState.DISLIKED),
                org.junit.jupiter.params.provider.Arguments.of("dl", LikeState.LIKED),
                org.junit.jupiter.params.provider.Arguments.of("ldd", LikeState.EMPTY),
                org.junit.jupiter.params.provider.Arguments.of("lldd", LikeState.EMPTY),
                org.junit.jupiter.params.provider.Arguments.of("ddl", LikeState.LIKED)
        );
    }

    @ParameterizedTest
    @MethodSource("provideMultiSlaps")
    void testMultiSlaps(String input, LikeState expectedFinal) {
        assertSame(expectedFinal, SlapThatLikeButton.slapMany(LikeState.EMPTY, input));
    }

    @Test
    void testDivideByZero() {
        assertThrows(ArithmeticException.class, () -> {
            int x = 1 / 0;
        });
    }

    @Test
    void testInvalidSlap() {
        Exception ex = assertThrows(IllegalArgumentException.class, () ->
            SlapThatLikeButton.slapMany(LikeState.EMPTY, "x"));
        assertTrue(ex.getMessage().toLowerCase().contains("invalid"));
    }

    @Test
    void testPrintCapture() {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        PrintStream orig = System.out;
        try {
            System.setOut(new PrintStream(out));
            System.out.print("hello");
        } finally {
            System.setOut(orig);
        }
        assertEquals("hello", out.toString());
    }
}