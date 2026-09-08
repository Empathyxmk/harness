package com.example.slapping.original;

import com.example.slapping.*;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import static org.junit.jupiter.api.Assertions.*;

import java.util.stream.Stream;

/**
 * Ported from tests/test_slap_that_like_button.py
 *
 * Tests for slap_like/dislike, state transitions, and slap_many.
 */
class TestSlapThatLikeButton {

    @Test
    void testSlapLikeTransitions() {
        // LikeState.empty -> liked
        assertSame(LikeState.LIKED, SlapThatLikeButton.slapLike(LikeState.EMPTY));
        // LikeState.liked -> empty
        assertSame(LikeState.EMPTY, SlapThatLikeButton.slapLike(LikeState.LIKED));
        // LikeState.disliked -> liked
        assertSame(LikeState.LIKED, SlapThatLikeButton.slapLike(LikeState.DISLIKED));
    }

    @Test
    void testSlapDislikeTransitions() {
        // LikeState.empty -> disliked
        assertSame(LikeState.DISLIKED, SlapThatLikeButton.slapDislike(LikeState.EMPTY));
        // LikeState.liked -> disliked
        assertSame(LikeState.DISLIKED, SlapThatLikeButton.slapDislike(LikeState.LIKED));
        // LikeState.disliked -> empty
        assertSame(LikeState.EMPTY, SlapThatLikeButton.slapDislike(LikeState.DISLIKED));
    }

    static Stream<org.junit.jupiter.params.provider.Arguments> provideOtherStatesSlapMany() {
        return Stream.of(
            org.junit.jupiter.params.provider.Arguments.of(LikeState.LIKED, "", LikeState.LIKED),
            org.junit.jupiter.params.provider.Arguments.of(LikeState.DISLIKED, "", LikeState.DISLIKED),
            org.junit.jupiter.params.provider.Arguments.of(LikeState.LIKED, "l", LikeState.EMPTY),   // liked->empty
            org.junit.jupiter.params.provider.Arguments.of(LikeState.LIKED, "d", LikeState.DISLIKED),// liked->disliked
            org.junit.jupiter.params.provider.Arguments.of(LikeState.LIKED, "ld", LikeState.DISLIKED), // liked->empty->disliked
            org.junit.jupiter.params.provider.Arguments.of(LikeState.DISLIKED, "l", LikeState.LIKED), // disliked->liked
            org.junit.jupiter.params.provider.Arguments.of(LikeState.DISLIKED, "d", LikeState.EMPTY), // disliked->empty
            org.junit.jupiter.params.provider.Arguments.of(LikeState.LIKED, "dl", LikeState.LIKED)     // liked->disliked->liked
        );
    }

    @ParameterizedTest
    @MethodSource("provideOtherStatesSlapMany")
    void testOtherStatesSlapMany(LikeState initial, String slapSeq, LikeState expectedFinal) {
        assertSame(expectedFinal, SlapThatLikeButton.slapMany(initial, slapSeq));
    }

    @Test
    void testSlapManyInvalidUppercase() {
        // Should handle upper/lower case correctly
        assertSame(LikeState.LIKED, SlapThatLikeButton.slapMany(LikeState.EMPTY, "L"));
        assertSame(LikeState.DISLIKED, SlapThatLikeButton.slapMany(LikeState.LIKED, "D"));
        assertSame(LikeState.LIKED, SlapThatLikeButton.slapMany(LikeState.DISLIKED, "L"));
        // Mixed case
        assertSame(LikeState.DISLIKED, SlapThatLikeButton.slapMany(LikeState.EMPTY, "lD"));
        assertSame(LikeState.LIKED, SlapThatLikeButton.slapMany(LikeState.LIKED, "Dl"));
    }

    static Stream<String> provideBadSlapManyInputs() {
        return Stream.of("x", "z", " ", "1", "-", "_", "LdX");
    }

    @ParameterizedTest
    @MethodSource("provideBadSlapManyInputs")
    void testSlapManyInvalidInputRaises(String badSlap) {
        Exception ex = assertThrows(IllegalArgumentException.class,
            () -> SlapThatLikeButton.slapMany(LikeState.EMPTY, badSlap));
        assertTrue(ex.getMessage().toLowerCase().contains("invalid"));
    }
}