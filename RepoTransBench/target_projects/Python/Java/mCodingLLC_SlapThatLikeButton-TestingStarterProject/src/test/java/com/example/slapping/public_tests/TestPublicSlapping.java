package com.example.slapping.public_tests;

import com.example.slapping.*;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import static org.junit.jupiter.api.Assertions.*;

import java.util.stream.Stream;

class TestPublicSlapping {

    @Test
    void testPublicAlternateLikesDislikes() {
        assertSame(LikeState.LIKED, SlapThatLikeButton.slapMany(LikeState.EMPTY, "ldld"));
        assertSame(LikeState.LIKED, SlapThatLikeButton.slapMany(LikeState.LIKED, "dldl"));
    }

    @Test
    void testPublicFullCycle() {
        assertSame(LikeState.DISLIKED, SlapThatLikeButton.slapMany(LikeState.LIKED, "ldl"));
    }

    @Test
    void testPublicInvalidSlapCharSequence() {
        Exception ex = assertThrows(IllegalArgumentException.class, () ->
            SlapThatLikeButton.slapMany(LikeState.EMPTY, "zqyz"));
        assertTrue(ex.getMessage().toLowerCase().contains("invalid"));
    }

    static Stream<org.junit.jupiter.params.provider.Arguments> provideAutoSlapCycles() {
        return Stream.of(
            org.junit.jupiter.params.provider.Arguments.of(4, "like", LikeState.EMPTY),
            org.junit.jupiter.params.provider.Arguments.of(5, "like", LikeState.LIKED),
            org.junit.jupiter.params.provider.Arguments.of(7, "dislike", LikeState.DISLIKED),
            org.junit.jupiter.params.provider.Arguments.of(0, "dislike", LikeState.EMPTY)
        );
    }

    @ParameterizedTest
    @MethodSource("provideAutoSlapCycles")
    void testPublicAutoSlapCycles(int num, String action, LikeState expected) {
        assertSame(expected, SlapThatLikeButton.autoSlap(num, action));
    }

    @Test
    void testPublicAutoSlapInvalidNum() {
        // In Java this is not possible because argument is always int.
        // Instead, we'll simulate with negative value to trigger an error if needed,
        // But in the actual logic, negative values just repeat zero times.
        // So, we skip the 'TypeError' test as not meaningful for strict Java typing.
    }
}